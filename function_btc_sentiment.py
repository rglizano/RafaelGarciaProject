# REDACTED
# REDACTED
# May 2019

import pandas as pd
import requests  # Used to request json data from URL
import json  # Used to load json data
from pandas.io.json import json_normalize  # Manipulate nested json data


# Retrieving BTC sentiment data (in json format) from URL
# Read more at https://alternative.me/crypto/fear-and-greed-index/
# limit=0 to retrieve all available data
btc_sent_url = 'https://api.alternative.me/fng/?limit=0'
btc_sent_raw = json.loads(requests.get(btc_sent_url).text)

# Normalizing to avoid problems with nested json data
df_btc_sent = json_normalize(btc_sent_raw['data'])

# Deleting unused column
# 'time_until_update' is the time left until next data update
df_btc_sent.drop('time_until_update', axis=1, inplace=True)

# Converting timestamp to datetime and normalizing
# (moving the time to midnight) to avoid time from being displayed
df_btc_sent['timestamp'] = pd.to_datetime(df_btc_sent['timestamp'], \
                                          unit='s').dt.normalize()

# Renaming columns
df_btc_sent.columns = ['date', 'btc_sent_value', 'btc_sent']

# Creating new dummy df and combining it to original df
df_btc_sent = df_btc_sent.join(pd.get_dummies(df_btc_sent['btc_sent']))

print(df_btc_sent.head(20))
