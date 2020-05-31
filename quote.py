'''
Get stock quote from Zacks
'''
from datetime import datetime
import os
import pytz
import requests
import urllib3
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import math

ZACKS_API_URL = ('https://www.zacks.com/stock/quote/{}')

def parse_content(symbol, res):
    if res != None:
        #print(res.status_code)
        #print(res.text)
        content = BeautifulSoup(res.content, 'lxml')
        rank_box = content.body.find('div', attrs={'class':'zr_rankbox'})
        #print(rank_box.prettify())
        rank_view = rank_box.find(class_='rank_view')
        #print(rank_view.prettify())
        rank_text = rank_view.get_text()
        #print(rank_text)
        if rank_text.find('1-Strong Buy') != -1:
            rank = "1-Strong Buy"
            icon_id = '01d'
        elif rank_text.find('2-Buy') != -1:
            rank = "2-Buy"
            icon_id = '02d'
        elif rank_text.find('3-Hold') != -1:
            rank = "3-Hold"
            icon_id = '04d'
        elif rank_text.find('4-Sell') != -1:
            rank = "4-Sell"
            icon_id = '11d'
        elif rank_text.find('5-Strong Sell') != -1:
            rank = "5-Strong Sell"
            icon_id = '13d'
        else:
            rank = "0-NA"
            icon_id = '01n'
        #find last price
        last_price = float(content.body.find('div', attrs={'id': 'get_last_price'}).get_text())
    else:
        rank = "0-NA"
        icon_id = '01n'
        last_price = 0.0

    #d = {'name': symbol, 'rank': rank, 'last_price': last_price}
    d = {'base': 'stations',
     'clouds': {'all': 90},
     'cod': 200,
     'coord': {'lat': 46.81, 'lon': -71.21},
     'dt': 1590446242,
     'id': 6325494,
     'main': {'feels_like': 19.87,
              'humidity': 43,
              'pressure': 1017,
              'temp': last_price,
              'temp_max': 23,
              'temp_min': 22},
     'name': symbol,
     'sys': {'country': rank,
             'id': 890,
             'sunrise': 1590397162,
             'sunset': 1590452679,
             'type': 1},
     'timezone': -14400,
     'visibility': 40233,
     'weather': [{'description': 'overcast clouds',
                  'icon': icon_id,
                  'id': 804,
                  'main': 'Clouds'}],
     'wind': {'deg': 270, 'speed': 3.6}
    }
    return d


def query_stock_urllib3(symbol):
    rank = "0-NA"
    try:
        http = urllib3.PoolManager()
        url = ZACKS_API_URL.format(symbol)
        print(url)
        res = http.request('GET', url)
    except HTTPError as http_err:
        print("HTTP error occurred: %s" %(http_err))  # Python 3.6
        res = None
    except Exception as err:
        print("Other error occurred: %s" %(err))  # Python 3.6
        res = None
    else:
        status = 200
        
    d = parse_content(symbol, res)
    return d
        
    
def query_stock(symbol):
    rank = "0-NA"
    try:
        print(ZACKS_API_URL.format(symbol))
        req_headers = {    'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip,deflate,br',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Cache-Control' : 'max-age=0',
                    'Connection': 'keep-alive',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36' }

        res = requests.get(ZACKS_API_URL.format(symbol), headers=req_headers)
    except HTTPError as http_err:
        print("HTTP error occurred: %s" %(http_err))  # Python 3.6
        res = None
    except Exception as err:
        print("Other error occurred: %s" %(err))  # Python 3.6
        res = None
    else:
        status = 200
        #print('Success!')
        
    d = parse_content(symbol, res)
    return d
    

