import requests


def convert_currency(charCode):
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    if response.status_code:
        data = response.json()
        valute = data.get('Valute')
        сurrency_code = valute.get(charCode)
        nominal = сurrency_code.get('Nominal')
        value = сurrency_code.get('Value')
        return nominal, value

if __name__ == '__main__':
    print(convert_currency())
