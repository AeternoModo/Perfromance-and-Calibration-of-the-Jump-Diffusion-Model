from decouple import config
import twelvedata 
import json
from pprint import pprint
import requests 
import pandas as pd
import time 


#
# Twelve Data (Stocks)
#


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



#
# Polygon (Options)
#

api_key = config("POLYGON_KEY")

def option_prices(obs_start,obs_end,strike_arr,T,symbol):
    '''
    obs_start: (day) from which day do we start observing. Example: "2026-09-14"
    obs_end: (day) on which day we stop
    strike_arr: strike price array
    T: date of expiration of the stock (in ticker format). Example: 260914
    symbol: ticker symbol
    '''

    #We include a timer to bypass data extraction restrictions, we can only extract 5 tickers' data per minute.
    timer = 0

    option_prices = []

    for strike in strike_arr:
        timer += 1
        if timer % 6 == 0:
            time.sleep(60)

        ticker = f"O:{symbol}{T}C{strike*1000:08d}"

        url = (
            f"https://api.massive.com/v2/aggs/ticker/"
            f"{ticker}/range/1/day/{obs_start}/{obs_end}"
        ) # The 1 day range is a requirement of the free subscription to Polygon services
    
        params = {
            "adjusted": "true",
            "sort": "asc",
            "limit": 10,
            "apiKey": api_key        
        }

        response = requests.get(url, params=params)

        if response.status_code == 200: #succesfully extracted data

            data = response.json()
            results = data.get("results", [])

            if results:
                bar = results[-1]


                print(
                    "Strike:", strike,
                    "Ticker:", ticker,
                    "Close:", bar["c"],
                    "Volume:", bar["v"]
                )

                option_prices.append(bar["c"])

        elif response.status_code == 404:
            print(f"Error: {ticker} not found!")

            
        elif response.status_code == 429:
            print(f"Error: Request Overflow")

    return option_prices


#Example:

# # Example:

# selected_contracts = [7550, 7575, 7600, 7625, 7650, 7675, 7700, 7725, 7750]

# option_price = option_prices("2026-09-11","2026-09-14",selected_contracts,260914,"SPXW")
