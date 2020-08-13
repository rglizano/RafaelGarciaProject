# REDACTED
# REDACTED
# May 2019

'''
############
## SET UP ##
############
'''
import pandas as pd
import pandas_datareader.data as get_data
from pandas.tseries.offsets import BDay
import datetime as dt
import time
import numpy as np
import locale
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from get_data import get_data_function as gdata
from get_date import get_date_function as gdate

# To avoid errors with Seaborn lib:
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Sets locale/currency to USD
locale.setlocale(locale.LC_ALL, '')

# Ignores division by 0 errors
warnings.filterwarnings("ignore")

# Lists for understanding user input
affirmation_list = ['Y', 'y', 'Yes', 'YES', 'yes']
negation_list = ['N', 'n', 'No', 'NO', 'no']
valid_answers = ['Y', 'y', 'Yes', 'YES', 'yes',
                 'N', 'n', 'No', 'NO', 'no']

# Explaining nature of script
print("------------------------------------------------")
print("This script will analyse the performance of a "
      "cryptocurrency portfolio")
print("------------------------------------------------")

'''
############
##  DATES ##
############
'''
previous_bday = pd.datetime.today() - BDay(1)
earliest_date = dt.datetime(2015, 8, 8)  # Earliest date with data available
default_initial_date = dt.datetime(2017, 2, 15)
default_final_date = dt.datetime(2019, 2, 15)
initial_date, final_date = gdate(default_initial_date, default_final_date)


'''
####################
## GATHERING DATA ##
####################
'''
df_data = gdata()
df_data = df_data[initial_date:final_date]


'''
######################
## ASSET ALLOCATION ##
######################
'''
# Default weights
btc_weight = 0.25
eth_weight = 0.25
xrp_weight = 0.25
ltc_weight = 0.25
total_weight = btc_weight + eth_weight + xrp_weight + ltc_weight

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
#############################
## CALCULATING PERFORMANCE ##
#############################
'''
# Adding LIBOR data to DataFrame
df_data['libor'] = get_data.DataReader('USDONTD156N', 'fred',
                                       earliest_date, previous_bday)
df_data.libor = (df_data.libor / 100) / 360

# Dropping non-trading days. Using FRED LIBOR dates as 'trading days'
df_data = df_data.dropna(subset=['libor'])

# Calculating asset market values inside DataFrame (only first row)
df_data['btc_value'] = btc_weight * 1000000 * (1 + df_data.btc_return)
df_data['eth_value'] = eth_weight * 1000000 * (1 + df_data.eth_return)
df_data['xrp_value'] = xrp_weight * 1000000 * (1 + df_data.xrp_return)
df_data['ltc_value'] = ltc_weight * 1000000 * (1 + df_data.ltc_return)

# Temp lists used only for calculating market values (all rows except first)
# These are later added to the DataFrame df_data as asset_value
btc_value_temp = [df_data.btc_value.values[0]]
eth_value_temp = [df_data.eth_value.values[0]]
xrp_value_temp = [df_data.xrp_value.values[0]]
ltc_value_temp = [df_data.ltc_value.values[0]]

# Loops used to calculate assets market value (all rows except first)
for i in range(1, len(df_data.index)):        # BTC calculation
    btc_value_temp.append(btc_value_temp[i-1] * (1 + df_data.btc_return[i]))
df_data['btc_value'] = btc_value_temp

for i in range(1, len(df_data.index)):        # ETH calculation
    eth_value_temp.append(eth_value_temp[i-1] * (1 + df_data.eth_return[i]))
df_data['eth_value'] = eth_value_temp

for i in range(1, len(df_data.index)):        # XRP calculation
    xrp_value_temp.append(xrp_value_temp[i-1] * (1 + df_data.xrp_return[i]))
df_data['xrp_value'] = xrp_value_temp

for i in range(1, len(df_data.index)):        # LTC calculation
    ltc_value_temp.append(ltc_value_temp[i-1] * (1 + df_data.ltc_return[i]))
df_data['ltc_value'] = ltc_value_temp

# Calculating portfolio returns and market value in DataFrame
df_data['port_value'] = df_data.btc_value + df_data.eth_value + \
                          df_data.xrp_value + df_data.ltc_value
df_data['port_return'] = (df_data.port_value /
                          df_data.port_value.shift(1)) - 1
df_data['port_return'].fillna(0, inplace=True)  # To avoid errors later
df_data['port_ex_return'] = df_data.port_return - df_data.libor

# Performance statistics
port_market_value = df_data.loc[final_date, 'port_value']
port_cumulative_return = (df_data['port_value'].iloc[-1] / 1000000) - 1
port_avg_return = np.average(df_data.port_return)
port_avg_ex_return = np.average(df_data.port_ex_return)
port_std_dev = df_data.port_return.std()
port_annual_std_dev = port_std_dev * np.sqrt(252)
sharpe_ratio = (port_avg_ex_return / port_std_dev) * np.sqrt(252)

def print_portfolio_performance():
    print("------------------------------------------------")
    print("Crypto portfolio performance from " +
          initial_date.strftime("%d %b %Y") + " to " +
          final_date.strftime("%d %b %Y"))
    print("------------------------------------------------")
    print("Initial market value = $1,000,000.00")
    print("Ending market value = " + str(locale.currency(port_market_value,
                                                         grouping=True)))
    print("Cumulative return = " + str('{:.2%}'.format(port_cumulative_return)))
    print("Average daily return = " + str('{:.2%}'.format(port_avg_return)))
    print("Average daily excess return = " +
          str('{:.2%}'.format(port_avg_ex_return)))
    print("Daily returns standard deviation = " +
          str('{:.2%}'.format(port_std_dev)))
    print("Annualised standard deviation = " +
          str('{:.2%}'.format(port_annual_std_dev)))
    print("Annualised Sharpe ratio = " + str('{:.3}'.format(sharpe_ratio)))
    print("------------------------------------------------")

# Requests user input
ask = input("Would you like to print the portfolio performance? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    print_portfolio_performance()


'''
##########################
## PLOTTING PERFORMANCE ##
##########################
'''
# Creating new Dataframes in "long" format instead of "wide" format
df_data_long_value = df_data[['btc_value', 'eth_value', 'xrp_value',
                              'ltc_value', 'port_value']].copy()
df_data_long_value.columns = ['BTC', 'ETH', 'XRP', 'LTC', 'Portfolio']
df_data_long_value = pd.melt(df_data_long_value.reset_index(), id_vars='date',
                             var_name='Asset', value_name='Market Value')
df_data_long_value.set_index('date', inplace=True)

df_data_long_return = df_data[['port_return']].copy()
df_data_long_return['average_daily_return'] = port_avg_return
df_data_long_return.columns = ['Portfolio Daily Return', 'Average Return']
df_data_long_return = pd.melt(df_data_long_return.reset_index(), id_vars='date',
                              var_name='Return Type', value_name='Return')
df_data_long_return.set_index('date', inplace=True)

# Adding 30-day rolling volatility to master Dataframe
df_data['port_30_day_std_dev'] = df_data.port_return.rolling(30).std()

def plot_portfolio_returns():
    # Plotting
    sns.set(style="darkgrid")
    plt.figure(figsize=(9, 7))
    plt.xlim(initial_date, final_date)
    pr = sns.lineplot(x='date', y='Return', hue='Return Type',
                      data=df_data_long_return.reset_index())
    sns.despine(offset=10, trim=True, left=True)
    pr.set_title("Portfolio Daily Return & Average Return")
    pr.set_xlabel("Date")
    pr.set_ylabel("Return")

    # Formatting axes
    pr.xaxis.set_major_locator(mdates.MonthLocator())
    pr.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    pr.yaxis.set_major_formatter(ticker.FuncFormatter('{0:.0%}'.format))
    plt.xticks(rotation=45)

    plt.tight_layout()

def plot_market_value():
    # Plotting
    sns.set(style="darkgrid")
    plt.figure(figsize=(9, 7))
    plt.xlim(initial_date, final_date)
    mv = sns.lineplot(x='date', y='Market Value', hue='Asset',
                      data=df_data_long_value.reset_index())
    sns.despine(offset=10, trim=True, left=True)
    mv.set_title("Portfolio & Assets Market Value")
    mv.set_xlabel("Date")
    mv.set_ylabel("Market Value")

    # Formatting axes
    mv.xaxis.set_major_locator(mdates.MonthLocator())
    mv.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    mv.yaxis.set_major_formatter(ticker.FuncFormatter('${:,.0f}'.format))
    plt.xticks(rotation=45)

    plt.tight_layout()

def plot_rolling_vol():
    # Plotting
    sns.set(style="darkgrid")
    plt.figure(figsize=(9, 7))
    plt.xlim(initial_date, final_date)
    pr = sns.lineplot(x='date', y='port_30_day_std_dev',
                      data=df_data.reset_index())
    sns.despine(offset=10, trim=True, left=True)
    pr.set_title("Portfolio 30-Day Rolling Volatility")
    pr.set_xlabel("Date")
    pr.set_ylabel("Volatility")

    # Formatting axes
    pr.xaxis.set_major_locator(mdates.MonthLocator())
    pr.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    pr.yaxis.set_major_formatter(ticker.FuncFormatter('{0:.2%}'.format))
    plt.xticks(rotation=45)

    plt.tight_layout()

# Requests user input
ask = input("Would you like to plot the portfolio returns? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    plot_portfolio_returns()

# Requests user input
ask = input("Would you like to plot the portfolio market value? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    plot_market_value()

# Requests user input
ask = input("Would you like to plot the rolling volatility? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    plot_rolling_vol()
