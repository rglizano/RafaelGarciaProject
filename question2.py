# REDACTED
# REDACTED
# May 2019

'''
############
## SET UP ##
############
'''
import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import statsmodels.formula.api as smf
from get_date import get_date_function as gdate
from get_data import get_data_function as gdata

# To avoid errors with Seaborn lib:
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Lists for understanding user input
affirmation_list = ['Y', 'y', 'Yes', 'YES', 'yes']
negation_list = ['N', 'n', 'No', 'NO', 'no']
valid_answers = ['Y', 'y', 'Yes', 'YES', 'yes',
                 'N', 'n', 'No', 'NO', 'no']

# Explaining nature of script
print("------------------------------------------------")
print("This script will analyse cryptocurrencies' performance "
      "and relationships on key and non-key event dates")
print("------------------------------------------------")


'''
###########
## DATES ##
###########
'''
default_initial_date = dt.datetime(2018, 1, 31)
default_final_date = dt.datetime(2019, 1, 31)
initial_date, final_date = gdate(default_initial_date, default_final_date)


'''
####################
## GATHERING DATA ##
####################
'''
# Key events are defined manually and retrieved in CSV format
# from a personal Github repository
df_key_events = pd.read_csv(#GITHUB_URL_REDACTED,
                            parse_dates=True, index_col=0)

# Adding a "1" value to all key events to distinguish them
df_key_events['key_event'] = 1

# Retrieving crypto data with get_data_function
df_data = gdata()

# Joining market data and key events Dataframes
df_data = df_data.join(df_key_events)

# Cleaning and preparing the master Dataframe
df_data = df_data[initial_date:final_date]      # Slicing dates
df_data.drop(columns=['long_event', 'short_event'], axis=1, inplace=True)

# Calculating returns on key event dates
df_data['btc_key_event_return'] = df_data['key_event'] * \
                                  df_data['btc_return']
df_data['btc_pos_event_return'] = df_data['positive_event'] * \
                                  df_data['btc_return']
df_data['btc_neg_event_return'] = df_data['negative_event'] * \
                                  df_data['btc_return']

# Creating Dataframe with only key event dates and non key event dates
df_data_key = df_data[pd.notnull(df_data['key_event'])]
df_data_not_key = df_data[pd.isnull(df_data['key_event'])]

# Adding column to master Dataframe for OLS regression
df_data['event_type_reg'] = df_data['event_type']
df_data['event_type_reg'] = df_data['event_type_reg'].fillna("No Event")


'''
#############################
## CALCULATING PERFORMANCE ##
#############################
'''
btc_key_total_return = df_data['btc_key_event_return'].sum()
btc_pos_total_return = df_data['btc_pos_event_return'].sum()
btc_neg_total_return = df_data['btc_neg_event_return'].sum()

btc_key_mean_return = df_data['btc_key_event_return'].mean()
btc_pos_mean_return = df_data['btc_pos_event_return'].mean()
btc_neg_mean_return = df_data['btc_neg_event_return'].mean()

btc_key_median_return = df_data['btc_key_event_return'].median()
btc_pos_median_return = df_data['btc_pos_event_return'].median()
btc_neg_median_return = df_data['btc_neg_event_return'].median()

btc_key_std_dev = df_data['btc_key_event_return'].std()
btc_pos_std_dev = df_data['btc_pos_event_return'].std()
btc_neg_std_dev = df_data['btc_neg_event_return'].std()

def print_btc_performance():
    print("------------------------------------------------")
    print("BTC performance from " + initial_date.strftime("%d %b %Y") +
          " to " + final_date.strftime("%d %b %Y"))
    print("------------------------------------------------")
    print("Total returns: ")
    print("During key event dates: " +
          "{:.2%}".format(btc_key_total_return))
    print("During positive key event dates: " +
          "{:.2%}".format(btc_pos_total_return))
    print("During negative key event dates: " +
          "{:.2%}".format(btc_neg_total_return))
    print("------------------------------------------------")
    print("Mean returns: ")
    print("During key event dates: " +
          "{:.2%}".format(btc_key_mean_return))
    print("During positive key event dates: " +
          "{:.2%}".format(btc_pos_mean_return))
    print("During negative key event dates: " +
          "{:.2%}".format(btc_neg_mean_return))
    print("------------------------------------------------")
    print("Median returns: ")
    print("During key event dates: " +
          "{:.2%}".format(btc_key_median_return))
    print("During positive key event dates: " +
          "{:.2%}".format(btc_pos_median_return))
    print("During negative key event dates: " +
          "{:.2%}".format(btc_neg_median_return))
    print("------------------------------------------------")
    print("Standard deviation: ")
    print("During key event dates: " +
          "{:.2%}".format(btc_key_std_dev))
    print("During positive key event dates: " +
          "{:.2%}".format(btc_pos_std_dev))
    print("During negative key event dates: " +
          "{:.2%}".format(btc_neg_std_dev))
    print("------------------------------------------------")

# Requests user input
ask = input("Would you like to print a summary of BTC's performance? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    print_btc_performance()


'''
##################################
## PLOTTING KEY EVENTS TIMELINE ##
##################################
'''
def plot_key_events_timeline():
    # Creating new column with static value (0) to plot horizontal line
    df_key_events['static'] = 0

    # Plotting
    plt.figure(figsize=(14, 9))
    plt.ylim(-50, 35)
    ke = sns.lineplot(x='date', y='static', data=df_key_events.reset_index())
    sns.despine(offset=10, trim=True, left=True)
    ke.set_title("Key Cryptocurrency Events")
    ke.set_xlabel("Date")
    ke.axes.get_yaxis().set_visible(False)

    # Formatting major and minor x-axis
    ke.xaxis.set_major_locator(mdates.YearLocator(month=7, day=4))
    ke.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ke.xaxis.set_minor_locator(mdates.MonthLocator())
    ke.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
    ke.tick_params(axis='x', which='major', pad=15, bottom=False)

    # Adding text labels
    y_pos1 = 1       # Initial y-axis position for positive events
    y_pos2 = -2       # Initial y-axis position for negative events

    for index, row in df_key_events.iterrows():
        if row['positive_event'] == 1:
            y_pos1 += 3
            ke.annotate(row['short_event'], xy=(index, row['static']),
                        xycoords='data', xytext=(index, y_pos1),
                        textcoords='data', horizontalalignment='center',
                        bbox=dict(boxstyle='round', fc='w', ec='gray'),
                        arrowprops=dict(color='steelblue', arrowstyle='->'))
        else:
            y_pos2 -= 3
            ke.annotate(row['short_event'], xy=(index, row['static']),
                        xycoords='data', xytext=(index, y_pos2),
                        textcoords='data', horizontalalignment='center',
                        bbox=dict(boxstyle='round', fc='w', ec='gray'),
                        arrowprops=dict(color='steelblue', arrowstyle='->'))

    # Adding labels to distinguish between event types
    ke.text(df_key_events.index[0], 30, "Positive Events", size=15,
            bbox=dict(boxstyle='round', fc='forestgreen', alpha=0.25))
    ke.text(df_key_events.index[0], -40, "Negative Events", size=15,
            bbox=dict(boxstyle='round', fc='firebrick', alpha=0.25))

# Requests user input
ask = input("Would you like to plot a timeline of the key crypto events? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    plot_key_events_timeline()


'''
############################
## PLOTTING DAILY RETURNS ##
############################
'''
def plot_daily_returns():
    # Plotting
    sns.set(style="darkgrid")
    plt.figure(figsize=(8, 7))
    plt.xlim(initial_date, final_date)
    rp = sns.scatterplot(x='date', y='btc_key_event_return', hue='event_type',
                     data=df_data.reset_index())
    sns.despine(offset=10, trim=True, left=True)
    rp.set_title("BTC Returns on Key Event Dates")
    rp.set_xlabel("Date")
    rp.set_ylabel("Returns")
    rp.axhline(y=0, xmin=0.0, xmax=1.0, color='b', alpha=0.5)
    rp.yaxis.set_major_formatter(FuncFormatter('{0:.0%}'.format))

    # Formatting major and minor x-axis
    rp.xaxis.set_major_locator(mdates.MonthLocator())
    rp.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    plt.xticks(rotation=45)

    plt.tight_layout()

# Requests user input
ask = input("Would you like to plot the daily returns of BTC? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    plot_daily_returns()


'''
###################################
## PLOTTING RETURNS DISTRIBUTION ##
###################################
'''
def plot_returns_distribution():
    # Plotting
    sns.set(color_codes=True)
    plt.figure(figsize=(5, 5))
    dp = sns.distplot(df_data_key['btc_key_event_return'],
                      bins=10, kde=True, rug=True)
    dp.set_title("Distribution of Returns on Key Event Dates")
    dp.set_xlabel("Return")
    dp.set_ylabel("Frequency")
    dp.xaxis.set_major_formatter(FuncFormatter('{0:.0%}'.format))
    plt.tight_layout()

# Requests user input
ask = input("Would you like to plot the distribution of BTC returns? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    plot_returns_distribution()


'''
###########################
## PLOTTING CORRELATIONS ##
###########################
'''
# Creating Dataframe with only returns on key event dates
# and non key event dates
df_data_key_ret = df_data_key.copy()
df_data_key_ret.drop(['btc_close', 'eth_close', 'ltc_close', 'xrp_close',
                      'nasdaq_close', 'positive_event', 'negative_event',
                      'event_type', 'key_event', 'btc_key_event_return',
                      'btc_pos_event_return', 'btc_neg_event_return'],
                     axis=1, inplace=True)
df_data_key_ret.columns = ['BTC', 'ETH', 'XRP', 'LTC', 'NASDAQ']
df_data_not_key_ret = df_data_not_key.copy()
df_data_not_key_ret.drop(['btc_close', 'eth_close', 'ltc_close', 'xrp_close',
                          'nasdaq_close', 'positive_event', 'negative_event',
                          'event_type', 'key_event', 'btc_key_event_return',
                          'btc_pos_event_return', 'btc_neg_event_return'],
                         axis=1, inplace=True)
df_data_not_key_ret.columns = ['BTC', 'ETH', 'XRP', 'LTC', 'NASDAQ']

# Creating new correlation Dataframes
df_key_corr = df_data_key_ret.copy().corr()
df_not_key_corr = df_data_not_key_ret.copy().corr()

def plot_correlation():
    # Plotting
    # Created 3 axes: The first 2 contain the matrices and the 3rd contains
    # the color scale. This is to ensure both matrices have the same width
    fig, (ax1, ax2, axcb) = plt.subplots(1, 3, figsize=(12, 6),
                                         gridspec_kw={'width_ratios':[1,1,0.05]})
    ax1.get_shared_y_axes().join(ax2)
    cp1 = sns.heatmap(df_key_corr, ax=ax1, annot=True, fmt='0.2', cmap='Blues',
                      cbar=False)
    cp2 = sns.heatmap(df_not_key_corr, ax=ax2, annot=True, fmt='0.2', cmap='Blues',
                      cbar_ax=axcb)
    cp1.set_title("Key Event Dates")
    cp2.set_title("Not Key Event Dates")
    cp2.set_ylabel('')
    cp2.set_yticks([])
    plt.show()

# Requests user input
ask = input("Would you like to plot correlation matrices? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    plot_correlation()


'''
#########################
## REGRESSION ANALYSIS ##
#########################
'''
def regression_btc():
    reg_btc = smf.ols(formula='btc_return ~ key_event + eth_return + '
                              'xrp_return + ltc_return + nasdaq_return',
                      data=df_data).fit()
    print(reg_btc.summary())

def regression_eth():
    reg_eth = smf.ols(formula='eth_return ~ key_event + btc_return + '
                              'xrp_return + ltc_return + nasdaq_return',
                      data=df_data).fit()
    print(reg_eth.summary())

def regression_xrp():
    reg_xrp = smf.ols(formula='xrp_return ~ key_event + btc_return + '
                              'eth_return + ltc_return + nasdaq_return',
                      data=df_data).fit()
    print(reg_xrp.summary())

def regression_ltc():
    reg_ltc = smf.ols(formula='ltc_return ~ key_event + btc_return + '
                              'eth_return + xrp_return + nasdaq_return',
                      data=df_data).fit()
    print(reg_ltc.summary())

def regression_nasdaq():
    reg_nasdaq = smf.ols(formula='nasdaq_return ~ key_event + btc_return + '
                                 'eth_return + ltc_return + xrp_return',
                         data=df_data).fit()
    print(reg_nasdaq.summary())

# Requests user input (BTC)
ask = input("Would you like to perform a regression analysis on BTC? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    regression_btc()

# Requests user input (ETH)
ask = input("Would you like to perform a regression analysis on ETH? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    regression_eth()

# Requests user input (XRP)
ask = input("Would you like to perform a regression analysis on XRP? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    regression_xrp()

# Requests user input (LTC)
ask = input("Would you like to perform a regression analysis on LTC? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    regression_ltc()

# Requests user input (NASDAQ)
ask = input("Would you like to perform a regression analysis on the NASDAQ? "
            "(Enter Y/N)")
while ask not in valid_answers:
    ask = input("I didn't understand that. Would you like to? (Enter Y/N)")
if ask in affirmation_list:
    regression_nasdaq()
