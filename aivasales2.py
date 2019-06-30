import requests
import pprint
import json

city1 = 'Екатеринбург'

#str(input('Из какого города?'))
city2 = 'Москва'
#str(input('Куда?'))

one_way = str(False)
def get_iata(city1, city2):
    spum = 'https://www.travelpayouts.com/widgets_suggest_params?q=Из%20' + \
        city1 + '%20в%20' + city2
    req = requests.get(spum)
    data = json.loads(req.text)
    origin = data['origin']['iata']
    destination = data['destination']['iata']
    return origin, destination


def get_min_price(city1, city2):
    origin, destination = get_iata(city1, city2)
    spum = 'http://min-prices.aviasales.ru/calendar_preload?origin=' +\
    origin + '&destination=' + destination + '&one_way=false' 
    req = requests.get(spum)
    data = json.loads(req.text)
    min_prices = []
    for price in data['best_prices']:
        min_prices.append(price['value'])
    min_index = min_prices.index(min(min_prices))
    return data['best_prices'][min_index]

my_best_price = get_min_price(city1, city2)
print('original:', city1, 'destination:', city2, end=' ')
print('data:', my_best_price['found_at'], 'min price:', my_best_price['value'])