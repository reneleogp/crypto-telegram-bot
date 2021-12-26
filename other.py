import os
import requests
import json
import math
import time
from millify import millify

WEB_API_KEY = os.environ['LCW_API_KEY']

headers = {
    'content-type': 'application/json',
    'x-api-key': WEB_API_KEY,
}
session = requests.Session()
session.headers.update(headers)

def list(limit):
    parameters = {
        "currency": "USD",
        "sort": "rank",
        "order": "ascending",
        "offset": 0,
        "limit": limit,
        "meta": False
    }
    url = 'https://api.livecoinwatch.com/coins/list'
    r = session.post(url, data=json.dumps(parameters))
    return r.json()


def single(coin, meta):
    parameters = {"currency": "USD", "code": coin, "meta": meta}
    url = 'https://api.livecoinwatch.com/coins/single'
    r = session.post(url, data=json.dumps(parameters))
    return r.json()


def overview():
    parameters = {"currency": "USD"}
    url = 'https://api.livecoinwatch.com/overview'
    r = session.post(url, data=json.dumps(parameters))
    return r.json()


def list_exchanges(limit):
    parameters = {
        "currency": "USD",
        "sort": "volume",
        "order": "descending",
        "offset": 0,
        "limit": limit,
        "meta": False
    }
    url = 'https://api.livecoinwatch.com/exchanges/list'
    r = session.post(url, data=json.dumps(parameters))
    return r.json()


def single_exchange(exchange):
    parameters = {"currency": "USD", "code": exchange, "meta": True}
    url = 'https://api.livecoinwatch.com/exchanges/single'
    r = session.post(url, data=json.dumps(parameters))
    return r.json()

def overview_history(code, start, end):
  parameters = {"code": code, "start": start, "end": end, "meta": False}
  url ="https://api.livecoinwatch.com/coins/single/history" 
  r = session.post(url, data=json.dumps(parameters))
  return r.json()

# Format line function
def format_line(name, val, money):
    if type(val) == int or type(val) == float:
        if val < 1:
            val = format(val, '.6f')
        else:
            val = millify(val, precision=2)

    return "{0}: {1}{2}\n".format(name, "$" if money else "", val)  

def get_nearest_less_element(sample,key):
  if key in sample:
    return sample[key]
  else:
    return sample[str(max(x for x in sample.keys() if int(x) < int(key)))]    



__1year = 31536000
__90days = 7776000
__30days = 2592000
__7days = 604800
__24hours = 86400
__1hour = 3600

def get_change(history):
  t = int(time.time())
  t*= 1000
  
  price= {}
  for element in history:
    price[element['date']] = element['rate']

t = int(time.time())
t*= 1000
print(t)
      