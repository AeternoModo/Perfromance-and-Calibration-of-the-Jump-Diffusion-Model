from decouple import config
import twelvedata 
import json
from pprint import pprint
import requests 
import pandas as pd

#API access
api_key = config('TWELVEDATA_KEY')

#test-params
symbol = 'AAPL'
interval = '1day'
start_date = '2023-01-01'
end_date = '2023-01-31'

base_erl = 'https://api.twelvedata.com/time_series'

params = {
    'symbol': symbol,
    'interval': interval,
    'start_date': start_date,
    'end_date': end_date,
    'apikey': api_key
}

#get request
response = requests.get(base_erl, params=params)

pprint(response.json())

#convert to dataframe
data = pd.DataFrame(response.json()['values'])
print(data)
