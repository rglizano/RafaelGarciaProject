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
print("This script will analyse trading strategies on BTC and ETH. "
      "The main trigger is defined as a >=10% drop in value")
print("------------------------------------------------")


'''
###########
## DATES ##
###########
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
df_data = df_data[['btc_return', 'eth_return']].copy()

# New column of returns for 50% investment in each asset
df_data['btc_eth_return'] = 0.5 * df_data.btc_return + \
                            0.5 * df_data.eth_return


'''
#########################
## DEFINING STRATEGIES ##
#########################
'''
# btc_strat: BTC drops 10% or more
df_data.loc[df_data.btc_return <= -0.1, 'btc_drop'] = 1

# eth_strat: ETH drops 10% or more
df_data.loc[df_data.eth_return <= -0.1, 'eth_drop'] = 1

# btc_eth_strat: BTC & ETH drop 10% or more
df_data.loc[(df_data.btc_drop == 1) & (df_data.eth_drop == 1),
            'btc_eth_drop'] = 1

# Filling NaNs
df_data.btc_drop = df_data.btc_drop.fillna(0)
df_data.eth_drop = df_data.eth_drop.fillna(0)
df_data.btc_eth_drop = df_data.btc_eth_drop.fillna(0)


'''
#############################
## CALCULATING PERFORMANCE ##
#############################
'''
# Investment amount
initial_market_value = float(input("Enter initial portfolio value: "))

# When any strategy triggers, long next day then hold cash until next trigger
df_data.loc[df_data.btc_drop.shift(1) == 1,
            'btc_strat_return'] = 1 * df_data.btc_return
df_data.loc[df_data.eth_drop.shift(1) == 1,
            'eth_strat_return'] = 1 * df_data.eth_return
df_data.loc[df_data.btc_eth_drop.shift(1) == 1,
            'btc_eth_strat_return'] = 1 * df_data.btc_eth_return

# Filling NaNs
df_data.btc_strat_return = df_data.btc_strat_return.fillna(0)
df_data.eth_strat_return = df_data.eth_strat_return.fillna(0)
df_data.btc_eth_strat_return = df_data.btc_eth_strat_return.fillna(0)

# Calculating market values (first row only)
df_data['btc_strat_value'] = initial_market_value * \
                             (1 + df_data.btc_strat_return)
df_data['eth_strat_value'] = initial_market_value * \
                             (1 + df_data.eth_strat_return)
df_data['btc_eth_strat_value'] = initial_market_value * \
                             (1 + df_data.btc_eth_strat_return)

# Temp lists used only for calculating market values (all rows except first)
# These are later added to the DataFrame df_data as asset_value
btc_strat_value_temp = [df_data.btc_strat_value.values[0]]
eth_strat_value_temp = [df_data.eth_strat_value.values[0]]
btc_eth_strat_value_temp = [df_data.btc_eth_strat_value.values[0]]

# Loops used to calculate assets market value (all rows except first)
for i in range(1, len(df_data.index)):        # BTC calculation
    btc_strat_value_temp.append(btc_strat_value_temp[i-1] *
                                (1 + df_data.btc_strat_return[i]))
df_data.btc_strat_value = btc_strat_value_temp

for i in range(1, len(df_data.index)):        # ETH calculation
    eth_strat_value_temp.append(eth_strat_value_temp[i-1] *
                                (1 + df_data.eth_strat_return[i]))
df_data.eth_strat_value = eth_strat_value_temp

for i in range(1, len(df_data.index)):        # BTC & ETH calculation
    btc_eth_strat_value_temp.append(btc_eth_strat_value_temp[i-1] *
                                (1 + df_data.btc_eth_strat_return[i]))
df_data.btc_eth_strat_value = btc_eth_strat_value_temp

# Calculating returns
btc_strat_cumulative_return = (df_data['btc_strat_value'].iloc[-1] /
                               initial_market_value) - 1
eth_strat_cumulative_return = (df_data['eth_strat_value'].iloc[-1] /
                               initial_market_value) - 1
btc_eth_strat_cumulative_return = (df_data['btc_eth_strat_value'].iloc[-1] /
                                   initial_market_value) - 1

def print_strats_returns():
    print("BTC strategy yields a cumulative return of: " +
          str('{:.2%}'.format(btc_strat_cumulative_return)))
    print("ETH strategy yields a cumulative return of: " +
          str('{:.2%}'.format(eth_strat_cumulative_return)))
    print("BTC & ETH strategy yields a cumulative return of: " +
          str('{:.2%}'.format(btc_eth_strat_cumulative_return)))
    print("------------------------------------------------")

# Requests user input
ask = input("Would you like to print a summary of the returns? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    print_strats_returns()

'''
##########################
## PLOTTING PERFORMANCE ##
##########################
'''
# Creating new Dataframes in "long" format instead of "wide" format
df_data_long_value = df_data[['btc_strat_value', 'eth_strat_value',
                              'btc_eth_strat_value']].copy()
df_data_long_value.columns = ['BTC Strategy', 'ETH Strategy',
                              'BTC & ETH Strategy']
df_data_long_value = pd.melt(df_data_long_value.reset_index(), id_vars='date',
                             var_name='Strategy', value_name='Market Value')
df_data_long_value.set_index('date', inplace=True)

df_data_long_return = df_data[['btc_strat_return', 'eth_strat_return',
                               'btc_eth_strat_return']].copy()
df_data_long_return.columns = ['BTC Strategy', 'ETH Strategy',
                               'BTC & ETH Strategy']
df_data_long_return = pd.melt(df_data_long_return.reset_index(), id_vars='date',
                              var_name='Strategy', value_name='Return')
df_data_long_return.set_index('date', inplace=True)

def plot_market_value():
    # Plotting
    sns.set(style="darkgrid")
    plt.figure(figsize=(9, 7))
    plt.xlim(initial_date, final_date)
    mv = sns.lineplot(x='date', y='Market Value', hue='Strategy',
                      data=df_data_long_value.reset_index())
    sns.despine(offset=10, trim=True, left=True)
    mv.set_title("Market Value Per Strategy")
    mv.set_xlabel("Date")
    mv.set_ylabel("Market Value")

    # Formatting axes
    mv.xaxis.set_major_locator(mdates.MonthLocator())
    mv.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    mv.yaxis.set_major_formatter(ticker.FuncFormatter('${:,.0f}'.format))

    plt.xticks(rotation=45)

    plt.tight_layout()

# Requests user input
ask = input("Would you like to plot the market value of each strategy? "
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
    pr = sns.lineplot(x='date', y='Return', hue='Strategy',
                      data=df_data_long_return.reset_index())
    sns.despine(offset=10, trim=True, left=True)
    pr.set_title("Returns Per Strategy")
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
