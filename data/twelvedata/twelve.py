from decouple import config
import twelvedata 
import json
from pprint import pprint
import requests 
import pandas as pd

#API access and url grab
api_key = config('TWELVEDATA_KEY')
base_url = 'https://api.twelvedata.com/time_series'

#Ticker-Class: Insert Variables for your stock of interest and output basic information as a pandas file
class StockTicker:
    def __init__(self,symbol,interval,start_date,end_date):
        self.symbol = symbol
        self.interval = interval
        self.start_date = start_date
        self.end_date = end_date

    def get_data(self,show=False):
        #parameters for the request
        params = {
            'symbol': self.symbol,
            'interval': self.interval,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'apikey': api_key,
            #'outputsize': 5000
        }

        #request to the API
        response = requests.get(base_url, params=params)
        data = pd.DataFrame(response.json()['values'])
        if show:
            print(data)
        return data

#Example of use
#stock1 = StockTicker(symbol='AAPL', interval='1day', start_date='2023-01-01', end_date='2023-01-31')
#data = stock1.get_data(show=True)



