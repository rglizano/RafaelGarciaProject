# REDACTED
# REDACTED
# May 2019


'''
############
## SET UP ##
############
'''
import pandas as pd
from pandas.tseries.offsets import BDay
import datetime as dt
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
print("This script will analyse a reverse MACD trading strategy "
      "in a cryptocurrency portfolio")
print("The maximum absolute exposure per asset is 25%")
print("------------------------------------------------")


'''
###########
## DATES ##
###########
'''
previous_bday = pd.datetime.today() - BDay(1)
earliest_date = dt.datetime(2015, 8, 8)  # Earliest date with data available
default_initial_date = dt.datetime(2016, 1, 1)
default_final_date = dt.datetime(2019, 4, 30)
initial_date, final_date = gdate(default_initial_date, default_final_date)

'''
####################
## GATHERING DATA ##
####################
'''
df_data = gdata()
df_data = df_data[initial_date:final_date]
df_data.drop(['nasdaq_close', 'nasdaq_return'], axis=1, inplace=True)


'''
########################
## GENERATING SIGNALS ##
########################
'''
# A signal is triggered when the MACD 9-day SMA crosses over the MACD
# A signal of 1 indicates a long position, -1 a short position, 0 no position

# BTC signals
df_data['btc_ema_26'] = df_data['btc_close']\
    .ewm(span=26, min_periods=26, adjust=False, ignore_na=False).mean()
df_data['btc_ema_12'] = df_data['btc_close']\
    .ewm(span=12, min_periods=26, adjust=False, ignore_na=False).mean()
df_data['btc_macd'] = df_data.btc_ema_12 - df_data.btc_ema_26
df_data['btc_macd_sma_9'] = df_data.btc_macd.rolling(9).mean()
df_data.loc[df_data.btc_macd_sma_9 > df_data.btc_macd, 'btc_signal'] = -1
df_data.loc[df_data.btc_macd_sma_9 < df_data.btc_macd, 'btc_signal'] = 1
df_data.loc[df_data.btc_macd_sma_9 == df_data.btc_macd, 'btc_signal'] = 0

# ETH signals
df_data['eth_ema_26'] = df_data['eth_close']\
    .ewm(span=26, min_periods=26, adjust=False, ignore_na=False).mean()
df_data['eth_ema_12'] = df_data['eth_close']\
    .ewm(span=12, min_periods=26, adjust=False, ignore_na=False).mean()
df_data['eth_macd'] = df_data.eth_ema_12 - df_data.eth_ema_26
df_data['eth_macd_sma_9'] = df_data.eth_macd.rolling(9).mean()
df_data.loc[df_data.eth_macd_sma_9 > df_data.eth_macd, 'eth_signal'] = -1
df_data.loc[df_data.eth_macd_sma_9 < df_data.eth_macd, 'eth_signal'] = 1
df_data.loc[df_data.eth_macd_sma_9 == df_data.eth_macd, 'eth_signal'] = 0

# XRP signals
df_data['xrp_ema_26'] = df_data['xrp_close']\
    .ewm(span=26, min_periods=26, adjust=False, ignore_na=False).mean()
df_data['xrp_ema_12'] = df_data['xrp_close']\
    .ewm(span=12, min_periods=26, adjust=False, ignore_na=False).mean()
df_data['xrp_macd'] = df_data.xrp_ema_12 - df_data.xrp_ema_26
df_data['xrp_macd_sma_9'] = df_data.xrp_macd.rolling(9).mean()
df_data.loc[df_data.xrp_macd_sma_9 > df_data.xrp_macd, 'xrp_signal'] = -1
df_data.loc[df_data.xrp_macd_sma_9 < df_data.xrp_macd, 'xrp_signal'] = 1
df_data.loc[df_data.xrp_macd_sma_9 == df_data.xrp_macd, 'xrp_signal'] = 0

# LTC signals
df_data['ltc_ema_26'] = df_data['ltc_close']\
    .ewm(span=26, min_periods=26, adjust=False, ignore_na=False).mean()
df_data['ltc_ema_12'] = df_data['ltc_close']\
    .ewm(span=12, min_periods=26, adjust=False, ignore_na=False).mean()
df_data['ltc_macd'] = df_data.ltc_ema_12 - df_data.ltc_ema_26
df_data['ltc_macd_sma_9'] = df_data.ltc_macd.rolling(9).mean()
df_data.loc[df_data.ltc_macd_sma_9 > df_data.ltc_macd, 'ltc_signal'] = -1
df_data.loc[df_data.ltc_macd_sma_9 < df_data.ltc_macd, 'ltc_signal'] = 1
df_data.loc[df_data.ltc_macd_sma_9 == df_data.ltc_macd, 'ltc_signal'] = 0

'''
#############################
## CALCULATING PERFORMANCE ##
#############################
'''
# Investment amount
initial_market_value = float(input("Enter initial portfolio value: "))

# When any strategy triggers, trade occurs one day later
df_data.loc[df_data.btc_signal.shift(1) != 0, 'btc_strat_return'] = \
    df_data.btc_signal.shift(1) * df_data.btc_return
df_data.loc[df_data.eth_signal.shift(1) != 0, 'eth_strat_return'] = \
    df_data.eth_signal.shift(1) * df_data.eth_return
df_data.loc[df_data.xrp_signal.shift(1) != 0, 'xrp_strat_return'] = \
    df_data.xrp_signal.shift(1) * df_data.xrp_return
df_data.loc[df_data.ltc_signal.shift(1) != 0, 'ltc_strat_return'] = \
    df_data.ltc_signal.shift(1) * df_data.ltc_return

# Filling NaNs
df_data.fillna(0, inplace=True)

# Calculating market values (first row only)
df_data['btc_strat_value'] = 0.25 * initial_market_value * \
                             (1 + df_data.btc_strat_return)
df_data['eth_strat_value'] = 0.25 * initial_market_value * \
                             (1 + df_data.eth_strat_return)
df_data['xrp_strat_value'] = 0.25 * initial_market_value * \
                             (1 + df_data.xrp_strat_return)
df_data['ltc_strat_value'] = 0.25 * initial_market_value * \
                             (1 + df_data.ltc_strat_return)

# Temp lists used only for calculating market values (all rows except first)
# These are later added to the DataFrame df_data as asset_value
btc_strat_value_temp = [df_data.btc_strat_value.values[0]]
eth_strat_value_temp = [df_data.eth_strat_value.values[0]]
xrp_strat_value_temp = [df_data.xrp_strat_value.values[0]]
ltc_strat_value_temp = [df_data.ltc_strat_value.values[0]]

# Loops used to calculate assets market value (all rows except first)
for i in range(1, len(df_data.index)):        # BTC calculation
    btc_strat_value_temp.append(btc_strat_value_temp[i-1] *
                                (1 + df_data.btc_strat_return[i]))
df_data.btc_strat_value = btc_strat_value_temp

for i in range(1, len(df_data.index)):        # ETH calculation
    eth_strat_value_temp.append(eth_strat_value_temp[i-1] *
                                (1 + df_data.eth_strat_return[i]))
df_data.eth_strat_value = eth_strat_value_temp

for i in range(1, len(df_data.index)):        # xrp calculation
    xrp_strat_value_temp.append(xrp_strat_value_temp[i-1] *
                                (1 + df_data.xrp_strat_return[i]))
df_data.xrp_strat_value = xrp_strat_value_temp

for i in range(1, len(df_data.index)):        # ltc calculation
    ltc_strat_value_temp.append(ltc_strat_value_temp[i-1] *
                                (1 + df_data.ltc_strat_return[i]))
df_data.ltc_strat_value = ltc_strat_value_temp

# Portfolio columns
df_data['port_value'] = df_data.btc_strat_value + df_data.eth_strat_value \
                        + df_data.xrp_strat_value + df_data.ltc_strat_value
df_data['port_return'] = (df_data.port_value /
                          df_data.port_value.shift(1)) - 1
df_data['port_return'].fillna(0, inplace=True)  # To avoid errors later
df_data['port_value'].fillna(0, inplace=True)  # To avoid errors later

# Calculating returns
port_cumulative_return = (df_data['port_value'].iloc[-1] /
                          initial_market_value) - 1

print("The strategy yields a cumulative return of: " +
      str('{:.2%}'.format(port_cumulative_return)))


'''
##########################
## PLOTTING PERFORMANCE ##
##########################
'''
# Creating new Dataframes in "long" format instead of "wide" format
df_data_long_value = df_data[['btc_strat_value', 'eth_strat_value',
                              'xrp_strat_value', 'ltc_strat_value',
                              'port_value']].copy()
df_data_long_value.columns = ['BTC', 'ETH', 'XRP', 'LTC', 'Portfolio']
df_data_long_value = pd.melt(df_data_long_value.reset_index(), id_vars='date',
                             var_name='Asset', value_name='Market Value')
df_data_long_value.set_index('date', inplace=True)

df_data_long_return = df_data[['btc_strat_return', 'eth_strat_return',
                               'xrp_strat_return', 'ltc_strat_return']].copy()
df_data_long_return.columns = ['BTC', 'ETH', 'XRP', 'LTC']
df_data_long_return = pd.melt(df_data_long_return.reset_index(), id_vars='date',
                              var_name='Asset', value_name='Return')
df_data_long_return.set_index('date', inplace=True)

def plot_market_value():
    # Plotting
    sns.set(style="darkgrid")
    plt.figure(figsize=(9, 7))
    plt.xlim(initial_date, final_date)
    mv = sns.lineplot(x='date', y='Market Value', hue='Asset',
                      data=df_data_long_value.reset_index())
    sns.despine(offset=10, trim=True, left=True)
    mv.set_title("Market Value Per Asset")
    mv.set_xlabel("Date")
    mv.set_ylabel("Market Value")

    # Formatting axes
    mv.xaxis.set_major_locator(mdates.MonthLocator())
    mv.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    mv.yaxis.set_major_formatter(ticker.FuncFormatter('${:,.0f}'.format))

    plt.xticks(rotation=45)

    plt.tight_layout()

# Requests user input
ask = input("Would you like to plot the market value of each asset? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    plot_market_value()

def plot_strategies_returns():
    # Plotting
    sns.set(style="darkgrid")
    plt.figure(figsize=(9, 7))
    plt.xlim(initial_date, final_date)
    pr = sns.lineplot(x='date', y='Return', hue='Asset',
                      data=df_data_long_return.reset_index())
    sns.despine(offset=10, trim=True, left=True)
    pr.set_title("Returns Per Asset")
    pr.set_xlabel("Date")
    pr.set_ylabel("Return")

    # Formatting axes
    pr.xaxis.set_major_locator(mdates.MonthLocator())
    pr.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    pr.yaxis.set_major_formatter(ticker.FuncFormatter('{0:.0%}'.format))
    plt.xticks(rotation=45)

    plt.tight_layout()

# Requests user input
ask = input("Would you like to plot the returns of each strategy? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    plot_strategies_returns()
