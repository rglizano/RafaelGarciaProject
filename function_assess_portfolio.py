# REDACTED
# REDACTED
# May 2019

import pandas as pd
import pandas_datareader.data as get_data
from pandas.io.json import json_normalize
from pandas.tseries.offsets import BDay
import json
import requests
import datetime as dt
import time
import numpy as np
import locale
import warnings
locale.setlocale(locale.LC_ALL, '')     # Sets locale/currency to USD
warnings.filterwarnings("ignore")       # Ignores division by 0 errors

'''
##################
## CRYPTO  DATA ##
##################
'''

# Retrieving 2,000 (daily) data points from the beginning of the script
# because the API doesn't allow retrievals between two dates.
# Data is truncated later.
# CryptoCompare API is used: https://min-api.cryptocompare.com/documentation

# URLS for 2,000 (daily) data points per asset
btc_url = ('https://min-api.cryptocompare.com/data/histoday?'
           'fsym=BTC&tsym=USD&limit=2000'
           #'&api_key= #REDACTED_API_KEY)

eth_url = ('https://min-api.cryptocompare.com/data/histoday?'
           'fsym=ETH&tsym=USD&limit=2000'
           #'&api_key= #REDACTED_API_KEY)

xrp_url = ('https://min-api.cryptocompare.com/data/histoday?'
           'fsym=XRP&tsym=USD&limit=2000'
           #'&api_key= #REDACTED_API_KEY)

ltc_url = ('https://min-api.cryptocompare.com/data/histoday?'
           'fsym=LTC&tsym=USD&limit=2000'
           #'&api_key= #REDACTED_API_KEY)

# Creation and cleaning of BTC DataFrame
raw_btc = json.loads(requests.get(btc_url).text)
df_btc = json_normalize(raw_btc['Data'])
df_btc.drop(['high', 'low', 'open', 'volumefrom', 'volumeto'],
            axis=1, inplace=True)
df_btc.columns = ['btc_close', 'date']
df_btc['date'] = pd.to_datetime(df_btc['date'], unit='s').dt.normalize()
df_btc.set_index('date', inplace=True)

# Creation and cleaning of ETH DataFrame
raw_eth = json.loads(requests.get(eth_url).text)
df_eth = json_normalize(raw_eth['Data'])
df_eth.drop(['high', 'low', 'open', 'volumefrom', 'volumeto'],
            axis=1, inplace=True)
df_eth.columns = ['eth_close', 'date']
df_eth['date'] = pd.to_datetime(df_eth['date'], unit='s').dt.normalize()
df_eth.set_index('date', inplace=True)

# Creation and cleaning of XRP DataFrame
raw_xrp = json.loads(requests.get(xrp_url).text)
df_xrp = json_normalize(raw_xrp['Data'])
df_xrp.drop(['high', 'low', 'open', 'volumefrom', 'volumeto'],
            axis=1, inplace=True)
df_xrp.columns = ['xrp_close', 'date']
df_xrp['date'] = pd.to_datetime(df_xrp['date'], unit='s').dt.normalize()
df_xrp.set_index('date', inplace=True)

# Creation and cleaning of LTC DataFrame
raw_ltc = json.loads(requests.get(ltc_url).text)
df_ltc = json_normalize(raw_ltc['Data'])
df_ltc.drop(['high', 'low', 'open', 'volumefrom', 'volumeto'],
            axis=1, inplace=True)
df_ltc.columns = ['ltc_close', 'date']
df_ltc['date'] = pd.to_datetime(df_ltc['date'], unit='s').dt.normalize()
df_ltc.set_index('date', inplace=True)

# Creating a single crypto DataFrame
df_data = df_btc.join([df_eth, df_xrp, df_ltc])


'''
###############
## VARIABLES ##
###############
'''

# Lists for understanding user input
affirmation_list = ['Y', 'y', 'Yes', 'YES', 'yes']
negation_list = ['N', 'n', 'No', 'NO', 'no']
valid_answers = ['Y', 'y', 'Yes', 'YES', 'yes', 'N', 'n', 'No', 'NO', 'no']

# Default dates
previous_bday = pd.datetime.today() - BDay(1)
earliest_date = dt.datetime(2015, 8, 8)  # Earliest date with data available
initial_date = dt.datetime(2017, 2, 15)
final_date = dt.datetime(2019, 2, 15)

# Default weights
btc_weight = 0.25
eth_weight = 0.25
xrp_weight = 0.25
ltc_weight = 0.25
total_weight = btc_weight + eth_weight + xrp_weight + ltc_weight


'''
###############
## FUNCTIONS ##
###############
'''

# Function for date user input
def input_date():
    date_is_valid = False
    new_date = ""
    while not date_is_valid:
        new_date = input("Remember to use d/m/y format:")
        try:
            # strptime will return an error if the input is incorrect
            new_date = dt.datetime.strptime(new_date, "%d/%m/%y")
            date_is_valid = True
        except ValueError:
            print("There seems to be an error!")
    return new_date

# Function for defining asset allocation
def input_weight():
    weight_is_valid = False
    weight = ""
    while not weight_is_valid:
        weight = input("Remember to use decimals: ")
        try:
            weight = float(weight)
            weight_is_valid = True
        except ValueError:
            print("There seems to be an error!")
    return weight


'''
####################
## DEFINING DATES ##
####################
'''

print("Welcome to the Crypto Portfolio Analyser 0.1")
time.sleep(0.75)
print("Let's start with the portfolio dates.")
time.sleep(0.75)

# Defining if initial date will change
print("The default initial date is " +
      str(dt.datetime.strftime(initial_date, "%d/%m/%y")))
time.sleep(0.75)
print("Would you like to change it? (Enter Y/N)")
change_date = input()

while change_date not in valid_answers:     # Checks if input is valid
    change_date = input("I didn't understand that. "
                        "Would you like to change it? (Enter Y/N)")

if change_date in affirmation_list:         # conditionals to change date
    print("Enter the new initial date.")    # and check for date validity
    initial_date = input_date()
    while initial_date < earliest_date:
        print("Invalid date. Initial date can't be earlier than "
              "8/8/15. There's not enough data before this date. Try again")
        initial_date = input_date()
        if initial_date >= earliest_date:
            break
    print("The new initial date is: " +
          initial_date.strftime('%d/%m/%y'))
elif change_date in negation_list:
    print("OK. The initial date will remain as " +
          initial_date.strftime('%d/%m/%y'))


# Defining if final date will change
time.sleep(0.75)
print("The default final date is " +
      str(dt.datetime.strftime(final_date, "%d/%m/%y")))
time.sleep(0.75)
print("Would you like to change it? (Enter Y/N)")
change_date = input()

while change_date not in valid_answers:     # Checks if input is valid
    change_date = input("I didn't understand that. "
                        "Would you like to change it? (Enter Y/N)")

if change_date in affirmation_list:         # Conditionals to change date
    print("Enter the new final date.")      # and check for date validity
    final_date = input_date()
    while final_date > previous_bday:
        print("Invalid date. The latest final date can only be the"
              "previous business day.")
        print("Remember the initial date is " +
              initial_date.strftime('%d/%m/%y') + ". Try again.")
        final_date = input_date()
        if final_date == previous_bday:
            break
    while final_date <= initial_date:
        print("Invalid date. The final date can't be equal or less "
              "than the initial date")
        print("Remember the initial date is " +
              initial_date.strftime('%d/%m/%y') + ". Try again.")
        final_date = input_date()
        if final_date > initial_date:
            break
    print("The new final date is: " + final_date.strftime('%d/%m/%y'))
else:
    print("OK. The final date will remain as " +
          final_date.strftime('%d/%m/%y'))


'''
######################
## ASSET ALLOCATION ##
######################
'''

time.sleep(0.75)
print("Let's move to asset allocation.")
print("Available assets are BTC, ETH, XRP, and LTC.")
print("Long and short positions are allowed, "
      "but portfolio total weight must be 1.0.")
print("Portfolio is currently equally-weighted (i.e. 25% for each asset).")
time.sleep(1)

# Defining if weights will change
change_weights = input("Would you like to change the default allocation?"
                       "(Enter Y/N)")

while change_weights not in valid_answers:     # Checks if input is valid
    change_weights = input("I didn't understand that. "
                           "Would you like to change it? (Enter Y/N)")

if change_weights in affirmation_list:          # Requests for input
    print("Enter the desired allocation in BTC.")
    btc_weight = input_weight()
    print("Enter the desired allocation in ETH.")
    eth_weight = input_weight()
    print("Enter the desired allocation in XRP.")
    xrp_weight = input_weight()
    print("Enter the desired allocation in LTC.")
    ltc_weight = input_weight()
    while total_weight != 1:                    # Checks for invalid weights
        print("Sorry, the weights don't add up to 1.00, try again.")
        print("Enter the desired allocation in BTC.")
        btc_weight = input_weight()
        print("Enter the desired allocation in ETH.")
        eth_weight = input_weight()
        print("Enter the desired allocation in XRP.")
        xrp_weight = input_weight()
        print("Enter the desired allocation in LTC.")
        ltc_weight = input_weight()
        if total_weight == 1:
            break


'''
#################
## PERFORMANCE ##
#################
'''
# Adding LIBOR data to DataFrame
df_data['libor'] = get_data.DataReader('USDONTD156N', 'fred',
                                         earliest_date, previous_bday)

# Dropping non-trading days. Using FRED LIBOR dates as 'trading days'
df_crypto = df_crypto.dropna(subset=['libor'])

# Calculating returns inside DataFrame
df_crypto['btc_return'] = np.log(df_btc.btc_close) - \
                       np.log(df_btc.btc_close.shift(1))
df_crypto['eth_return'] = np.log(df_eth.eth_close) - \
                       np.log(df_eth.eth_close.shift(1))
df_crypto['xrp_return'] = np.log(df_xrp.xrp_close) - \
                       np.log(df_xrp.xrp_close.shift(1))
df_crypto['ltc_return'] = np.log(df_ltc.ltc_close) - \
                       np.log(df_ltc.ltc_close.shift(1))

# Calculating asset market values inside DataFrame (only first row)
df_crypto['btc_value'] = btc_weight * 1000000 * (1 + df_crypto.btc_return)
df_crypto['eth_value'] = eth_weight * 1000000 * (1 + df_crypto.eth_return)
df_crypto['xrp_value'] = xrp_weight * 1000000 * (1 + df_crypto.xrp_return)
df_crypto['ltc_value'] = ltc_weight * 1000000 * (1 + df_crypto.ltc_return)

# Temp lists used only for calculating market values (all rows except first)
# These are later added to the DataFrame dt_crypto as asset_value
btc_value_temp = [df_crypto.btc_value.values[0]]
eth_value_temp = [df_crypto.eth_value.values[0]]
xrp_value_temp = [df_crypto.xrp_value.values[0]]
ltc_value_temp = [df_crypto.ltc_value.values[0]]

# Loops used to calculate assets market value (all rows except first)
for i in range(1, len(df_crypto.index)):        # BTC calculation
    btc_value_temp.append(btc_value_temp[i-1] * (1 + df_crypto.btc_return[i]))
df_crypto['btc_value'] = btc_value_temp

for i in range(1, len(df_crypto.index)):        # ETH calculation
    eth_value_temp.append(eth_value_temp[i-1] * (1 + df_crypto.eth_return[i]))
df_crypto['eth_value'] = eth_value_temp

for i in range(1, len(df_crypto.index)):        # XRP calculation
    xrp_value_temp.append(xrp_value_temp[i-1] * (1 + df_crypto.xrp_return[i]))
df_crypto['xrp_value'] = xrp_value_temp

for i in range(1, len(df_crypto.index)):        # LTC calculation
    ltc_value_temp.append(ltc_value_temp[i-1] * (1 + df_crypto.ltc_return[i]))
df_crypto['ltc_value'] = ltc_value_temp

# Slicing DataFrame
df_crypto = df_crypto[initial_date:final_date]

# Calculating portfolio returns and market value in DataFrame
df_crypto['port_value'] = df_crypto.btc_value + df_crypto.eth_value + \
                          df_crypto.xrp_value + df_crypto.ltc_value
df_crypto['port_return'] = np.log(df_crypto.port_value) - \
                           np.log(df_crypto.port_value.shift(1))
df_crypto['port_value'].fillna(0, inplace=True)   # To avoid errors later
df_crypto['port_return'].fillna(0, inplace=True)  # To avoid errors later

# New variables of final results
port_cumulative_return = str('{:.2%}'.format(sum(df_crypto.port_return)))
port_market_value = str(locale.currency(df_crypto.loc
                                        [final_date, 'port_value'],
                                        grouping=True))
port_avg_return = np.average(df_crypto.port_return)
port_std_dev = df_crypto.port_return.std()
sharpe_ratio = (port_avg_return / port_std_dev) * np.sqrt(252)
df_crypto['port_30_day_std_dev'] = df_crypto.port_return.rolling(30).std()

# Printing results
print("The following are the portfolio statistics: ")
print("Initial market value = $1,000,000.00")
print("Ending market value = " + port_market_value)
print("Cumulative return = " + port_cumulative_return)
print("Average daily return = " + str('{:.2%}'.format(port_avg_return)))
print("Average annual return = ")
print("Total standard deviation = " + str('{:.2%}'.format(port_std_dev)))
print("Annualised standard deviation = ")
print("Annualised Sharpe ratio = " + str(sharpe_ratio))

