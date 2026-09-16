from decouple import config
import twelvedata 
import json
from pprint import pprint
import requests 
import pandas as pd
import numpy as np
import time 


#
# Twelve Data (Stocks)
#


#API access and url grab
api_key_twelve = config('TWELVEDATA_KEY')
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
            'apikey': api_key_twelve,
            #'outputsize': 5000
        }

        #request to the API
        response = requests.get(base_url, params=params)
        data = pd.DataFrame(response.json()['values'])
        if show:
            print(data)
        return data

    def get_close(self):
        data = self.get_data()
        return data['close']

#Example of use
#stock1 = StockTicker(symbol='AAPL', interval='1day', start_date='2023-01-01', end_date='2023-01-31')
#data = stock1.get_data(show=True)



#
# Polygon (Options)
#

api_key_polygon = config("POLYGON_KEY")

def strikeprice_gen(S1,steps,percent,offset):
    '''
    steps: Distance between prices of the strike array
    S1: Value of the underlying 
    percent: percent away from in the money (ITM), start of the range  
    offset: perecent away from ITM, end of range

    Algorithm:

    We take the price of an asset at closure "S1" and create an array of step "steps"
    at "percent" percent away from "S1". We then omit the "offset" percent 
    away from "S1".

    Example:
    A stock has a final price of S1 = 7754. I only really care what happens within a range 
    of percent = 2% away from ITM and on intervals of step = 25chf. I take:    
    
    strikeprice_gen_ATM(25,7611.44,0.02,0)
    and get: 
    [7450. 7475. 7500. 7525. 7550. 7575. 7600.]

    But now I don't actually want the first few terms because my model doesn't work 
    so well there. I set offset = 0.5%. Therefore I take:

    strikeprice_gen_ATM(25,7611.44,0.02,0)
    and get: 
    [7450. 7475. 7500. 7525. 7550.]   
    '''

    range_strikes = S1 * percent # range in which we generate our strike prices
    range_stikes_offset = S1 * offset # range in which we generate our strike prices

    strike_arr = np.arange(round((S1 - range_strikes) / steps) * steps, S1 - range_stikes_offset , steps)

    return strike_arr



def option_prices_1d(obs_start,obs_end,T,symbol_options,S1,steps,percent,offset):
    '''
    obs_start: From which day do we start observing. Example: "2026-09-14"
    obs_end: On which day we stop observing.
    strike_arr: Strike price array
    T: Date of expiration of the stock (in ticker format). Example: 260914
    symbol_option: Options ticker symbol. Example: SPXW
    steps: Distance between prices of the strike array

    We observe the data on one day. For a strike on the closure of that day
    '''

    #We include a timer to bypass data extraction restrictions, we can only extract 5 tickers' data per minute.
    timer = 0


    strike_arr = strikeprice_gen(S1,steps,percent,offset)

    print("List of strikes:", strike_arr)

    option_prices = []

    for strike in strike_arr:
        timer += 1
        if timer % 5 == 0:
            time.sleep(60)

        ticker = f"O:{symbol_options}{T}C{int(strike*1000):08d}"

        url = (
            f"https://api.massive.com/v2/aggs/ticker/"
            f"{ticker}/range/1/day/{obs_start}/{obs_end}"
        ) # The 1 day range is a requirement of the free subscription to Polygon services
    
        params = {
            "adjusted": "true",
            "sort": "asc",
            "limit": 10,
            "apiKey": api_key_polygon
        }

        response = requests.get(url, params=params)

        if response.status_code == 200: #succesfully extracted data

            data = response.json()
            results = data.get("results", [])

            if results:
                bar = results[0]


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
            print("Error: Request Overflow")

        else:
            print("Something's wrong...",response.status_code)

    return option_prices, strike_arr



