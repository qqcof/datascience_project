import requests

from config import symbol_tiker, API_KEY


def get_and_save_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={api_key}&datatype=csv'
    response = requests.get(url)

    if response.status_code == 200:
        with open('nvda_data.csv', 'wb') as f:
            f.write(response.content)

        print('Данные успешно записаны в csv файл!')
    else:
        print('Ошибка получения данных!')


if __name__ == '__main__':
    symbol = symboltiker
    api_key = apikey
    get_and_save_data(symbol, api_key)
