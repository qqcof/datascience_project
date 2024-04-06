import config
import json
import requests


def format_data(monthly_time_series):
    formatted_data = []

    for date, values in monthly_time_series.items():
        timestamp = date
        open_price = values['1. open']
        high_price = values['2. high']
        low_price = values['3. low']
        close_price = values['4. close']
        volume = values['5. volume']

        formatted_data.append({
            'Timestamp': timestamp,
            'Open': open_price,
            'High': high_price,
            'Low': low_price,
            'Close': close_price,
            'Volume': volume
        })

    return formatted_data


def get_and_save_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={api_key}&datatype=json'
    response = requests.get(url)
    data = response.json()

    if 'Monthly Time Series' in data:
        monthly_time_series = data['Monthly Time Series']
        formatted_data = format_data(monthly_time_series)

        with open('nvda_data_formatted.json', 'w') as formatted_file:
            json.dump(formatted_data, formatted_file, indent=4)

        print('Данные успешно записаны в json файл!')
    else:
        print('Ошибка получения данных!')


if __name__ == '__main__':
    symbol = config.symboltiker
    api_key = config.apikey
    get_and_save_data(symbol, api_key)
