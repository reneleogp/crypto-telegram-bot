import os
import requests
import json

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


def single(coin):
    parameters = {"currency": "USD", "code": coin, "meta": True}
    url = 'https://api.livecoinwatch.com/coins/single'
    r = session.post(url, data=json.dumps(parameters))
    return r.json()
