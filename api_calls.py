import os
import requests

from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

WEB_API_KEY = os.environ['CRYPTO_WEB_API_KEY']


headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': WEB_API_KEY,
}

session = requests.Session()
session.headers.update(headers)


parameters = {
  'start':'1',
  'limit':'1',
  'convert':'USD'
}
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

try:
  response = session.get(url, params=parameters)  
  data = json.loads(response.text)
  print(response.json())
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
  