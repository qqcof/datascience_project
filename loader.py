import config
import get_data_json
import psycopg2
from datetime import datetime


def create_table_sql(table_name):
    sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        timestamp DATE,
        open_price NUMERIC,
        high_price NUMERIC,
        low_price NUMERIC,
        close_price NUMERIC,
        volume NUMERIC
    )
    """
    return sql


def insert_data_sql(table_name):
    sql = f"""
    INSERT INTO {table_name} (timestamp, open_price, high_price, low_price, close_price, volume)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    return sql


def load_data():
    connect = psycopg2.connect(
        dbname=config.dbname,
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port
    )

    cur = connect.cursor()

    table_name = config.tablename
    cur.execute(create_table_sql(table_name))

    connect.commit()

    formatted_data = get_data_json.get_and_save_data(config.symboltiker, config.apikey)
    if formatted_data:
        for row in formatted_data:
            timestamp = datetime.strptime(row['Timestamp'], '%Y-%m-%d').date()
            open_price = row['Open']
            high_price = row['High']
            low_price = row['Low']
            close_price = row['Close']
            volume = row['Volume']

            cur.execute(insert_data_sql(table_name), (timestamp, open_price, high_price, low_price, close_price, volume))

        connect.commit()
        cur.close()
        connect.close()

        print('Данные успешно загружены в базу данных PostgreSQL!')
    else:
        print('Отсутствуют данные для загрузки в базу данных!')


if __name__ == '__main__':
    load_data()
