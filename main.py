import requests, json, os
import argparse
from dotenv import load_dotenv
load_dotenv()
from urllib.parse import urlparse


BITLY_TOKEN = os.getenv('BITLY_TOKEN')
BITLY_SHORTEN_API_URL = 'https://api-ssl.bitly.com/v4/shorten'
def shorten_link(BITLY_TOKEN, LONG_URL):
  headers ={'Authorization': f'Bearer {BITLY_TOKEN}'}
  params = {
    "long_url": f"{LONG_URL}"
  }
  response = requests.post(BITLY_SHORTEN_API_URL, headers=headers, json=params)
  response.raise_for_status()
  bitly_link = response.json()
  return bitly_link['link']


def count_clicks(BITLY_TOKEN, LONG_URL):
  bitlink = (shorten_link(BITLY_TOKEN, LONG_URL))
  bitlink = bitlink.replace('http://','')
  headers ={'Authorization': f'Bearer {BITLY_TOKEN}'}  
  total_click = { 
          "unit": "day",
          "units": "-1"
  }
  clicks_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
  response = requests.get(clicks_url, headers=headers, params=total_click)
  response.raise_for_status()
  bitly_response = response.json()
  return bitly_response['total_clicks']

   
if __name__ == '__main__':

   parser = argparse.ArgumentParser()
   parser.add_argument('url')
   args = parser.parse_args()
  
   try:
    print('Короткая ссылка: ', shorten_link(BITLY_TOKEN , args.url))
   except requests.exceptions.HTTPError:
     print("err")

   try:
       print('По вашей ссылке прошли', count_clicks(BITLY_TOKEN, args.url), 'раз')
   except requests.exceptions.HTTPError:
      print("err")
