import os
import requests
import json
import math
import time
from millify import millify

WEB_API_KEY = os.environ['LCW_API_KEY']

dists = {
    "1 Year": 31536000000,
    "90 Days": 7776000000,
    "30 Days": 2592000000,
    "7 Days": 604800000,
    "24 Hours": 86400000,
    "1 Hour": 3600000
}

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
    url = "https://api.livecoinwatch.com/coins/single/history"
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


def get_nearest_less_element(sample, key):
    if key in sample:
        return sample[key]
    else:
        return sample[str(max(x for x in sample.keys() if int(x) < int(key)))]


def get_change(changes, timeframe, code):
    t = int(time.time())
    t *= 1000

    start = t - (dists[timeframe] + dists["1 Hour"])
    end = t - (dists[timeframe])

    if timeframe == "1 Hour" or timeframe == "24 Hours":
      start += dists["1 Hour"]
      end = t

    

    r = overview_history(code, start, end)
    try:
        changes[timeframe] = r['history'][0]['rate']
    except Exception:
        changes[timeframe] = None