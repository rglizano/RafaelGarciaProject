import json
import numpy as np
import configparser
import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
from oanda_functions import get_nav
from oanda_functions import save_tick_data
from oanda_functions import get_open_positions
from oanda_functions import get_trade_details
from oanda_functions import submit_buy
from oanda_functions import submit_sell
# TODO import oanda_functions as oandaf
'''
##########
# SET UP #
##########
'''
config = configparser.ConfigParser()
config.read('oanda.ini')
account_id = config['oanda']['account_id']
access_token = config['oanda']['api_key']
api = API(access_token=access_token)
client = oandapyV20.API(access_token=access_token)


'''
#############
# VARIABLES #
#############
'''
trade_size = 1000000            # Update this
instrument = 'AUD_CAD'          # Update this
short_ticks = 5
long_ticks = 10
tick_number = 0
mid_price_list = []
initial_balance = get_nav(client, account_id)

'''
###############
# TRADING BOT #
###############
'''
# Initialises data stream
stream = pricing.PricingStream(accountID=account_id,
                               params={"instruments": instrument})
stream_request = api.request(stream)

# TODO Create function within function for printing all 3 lines of NAV
# TODO DO ABOVE and then add PNL as percentage as well as $$$$$
# TODO format (all) numbers (NAV/PNL)

# TODO do everything in a DataFrame and RESAMPLE to 10 seconds

# TODO CREATE A CLASS that includes functions that are together
# Trading bot
for tick in stream.response:
    tick_data = json.dumps(tick)            # Dict to string
    tick_data = json.loads(tick_data)       # String to JSON
    print("----------------")

    if len(tick_data) > 2:   # len > 2 indicates price was retrieved
        tick_number += 1
        print("Tick number: " + str(tick_number))
        # Save tick data into list
        mid_price_list = save_tick_data(tick_data, mid_price_list)
        # Calculate SMAs
        sma_short = np.average(mid_price_list[(-1 * short_ticks):])
        sma_long = np.average(mid_price_list[(-1 * long_ticks):])
        # Retrieve open positions
        position = get_open_positions(client, account_id, instrument)
        # Buy, sell or hold
        if sma_short > sma_long and position <= 0 \
                and tick_number > long_ticks:
            submit_buy(client, account_id, trade_size, instrument)
            get_trade_details(client, account_id, instrument)
            print("Initial NAV: " + str(initial_balance))
            print("Current NAV: " + str(get_nav(client, account_id)))
            print("PnL: " + str(get_nav(client, account_id) -
                                initial_balance))
            continue
        elif sma_short < sma_long and position >= 0 \
                and tick_number > long_ticks:
            submit_sell(client, account_id, trade_size, instrument)
            get_trade_details(client, account_id, instrument)
            print("Initial NAV: " + str(initial_balance))
            print("Current NAV: " + str(get_nav(client, account_id)))
            print("PnL: " + str(get_nav(client, account_id) -
                                initial_balance))
            continue
        else:
            print("Hold.")
            print("Initial NAV: " + str(initial_balance))
            print("Current NAV: " + str(get_nav(client, account_id)))
            print("PnL: " + str(get_nav(client, account_id) -
                                initial_balance))
            continue
    else:
        print("Heartbeat.")
        continue
