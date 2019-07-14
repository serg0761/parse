from zeep import Client
from datetimerange import DateTimeRange
import datetime
from pymongo import MongoClient


def dateRange(start, end):
    rangeList = []
    time_range = DateTimeRange(start, end)
    for value in time_range.range(datetime.timedelta(days=1)):
        rangeList.append(value.strftime('%Y-%m-%d'))
    return rangeList


def get_curs(date, currency, url):
    client = Client(url)
    money = client.service.GetCursOnDate(str(date))
    list_money=money._value_1._value_1
    for item in list_money:
        for k,v in item.items():
            if v.VchCode == currency:
                cur = item['ValuteCursOnDate']['Vcurs']
    return {'date': date, 'curs':float(cur)}


def get_date_to_mongo(start, end, currency, url):
    curses = []
    dates = dateRange(start, end)
    for date in dates:
        curs = get_curs(date, currency, url)
        curses.append(curs)  
    return curses


def find_date_min(curses):
    min_curs = float('inf')
    min_date = ''
    for curs in curses:
        if min_curs > curs['curs']:
            min_curs = curs['curs']
            min_date = curs['date']
    return min_date


def find_date_max(curses):
    max_curs = 0
    max_date = ''
    for curs in curses:
        if max_curs < curs['curs']:
            max_curs = curs['curs']
            max_date = curs['date']
    return max_date
    
 

def get_min_max_from_mongo(start, end, client):
    curses1 = list(client.find(({'date':{'$gte': start}})))
    min_date = find_date_min(curses1)
    curses2 = list(client.find(({'date':{'$gte': min_date}})))
    max_date = find_date_max(curses2)
    return (min_date, max_date)


start = "2018-01-01"
finish =  "2018-12-31"
url = 'https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL'


cur= get_date_to_mongo(start, finish, 'TMT', url)

client = MongoClient('mongodb://127.0.0.1:27017')

db = client['curses']
cursdb = db.curses
cursdb.insert_many(cur)


min_date, max_date = get_min_max_from_mongo(start, finish, cursdb)

print(f'Валюту стоило покупать {min_date}')
print(f'А затем, лучше всего было продать {max_date}')
