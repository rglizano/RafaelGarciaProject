# REDACTED
# REDACTED
# May 2019

import pandas as pd
from pandas.io.json import json_normalize
import json
import requests
import quandl

def get_data_function():

    '''
    #################
    ## EQUITY DATA ##
    #################
    '''
    # Requesting Nasdaq Composite EoD data from Quandl
    # Requesting "Index Value" only
    df_nasdaq = quandl.get("NASDAQOMX/COMP.1", authtoken=#REDACTED_TOKEN)
    df_nasdaq.columns = ['nasdaq_close']


    '''
    ##################
    ## CRYPTO  DATA ##
    ##################
    '''

    # Retrieving 2,000 (max) daily data points
    # CryptoCompare API is used: https://min-api.cryptocompare.com/documentation

    # URLS per asset
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
    df_btc = df_btc[df_btc['btc_close'] != 0]

    # Creation and cleaning of ETH DataFrame
    raw_eth = json.loads(requests.get(eth_url).text)
    df_eth = json_normalize(raw_eth['Data'])
    df_eth.drop(['high', 'low', 'open', 'volumefrom', 'volumeto'],
                axis=1, inplace=True)
    df_eth.columns = ['eth_close', 'date']
    df_eth['date'] = pd.to_datetime(df_eth['date'], unit='s').dt.normalize()
    df_eth.set_index('date', inplace=True)
    df_eth = df_eth[df_eth['eth_close'] != 0]

    # Creation and cleaning of XRP DataFrame
    raw_xrp = json.loads(requests.get(xrp_url).text)
    df_xrp = json_normalize(raw_xrp['Data'])
    df_xrp.drop(['high', 'low', 'open', 'volumefrom', 'volumeto'],
                axis=1, inplace=True)
    df_xrp.columns = ['xrp_close', 'date']
    df_xrp['date'] = pd.to_datetime(df_xrp['date'], unit='s').dt.normalize()
    df_xrp.set_index('date', inplace=True)
    df_xrp = df_xrp[df_xrp['xrp_close'] != 0]

    # Creation and cleaning of LTC DataFrame
    raw_ltc = json.loads(requests.get(ltc_url).text)
    df_ltc = json_normalize(raw_ltc['Data'])
    df_ltc.drop(['high', 'low', 'open', 'volumefrom', 'volumeto'],
                axis=1, inplace=True)
    df_ltc.columns = ['ltc_close', 'date']
    df_ltc['date'] = pd.to_datetime(df_ltc['date'], unit='s').dt.normalize()
    df_ltc.set_index('date', inplace=True)
    df_ltc = df_ltc[df_ltc['ltc_close'] != 0]


    '''
    ###############################
    ## CREATING MASTER DATAFRAME ##
    ###############################
    '''

    # Creating single Dataframe
    df_data = df_btc.join([df_eth, df_xrp, df_ltc, df_nasdaq])

    # Filling Nasdaq weekends with previous day data
    df_data['nasdaq_close'].fillna(method='ffill', inplace=True)

    # Converting Date to DateTime
    df_data.index = pd.to_datetime(df_data.index)

    # Calculating returns for all assets
    df_data['btc_return'] = (df_data.btc_close /
                             df_data.btc_close.shift(1)) - 1
    df_data['eth_return'] = (df_data.eth_close /
                             df_data.eth_close.shift(1)) - 1
    df_data['xrp_return'] = (df_data.xrp_close /
                             df_data.xrp_close.shift(1)) - 1
    df_data['ltc_return'] = (df_data.ltc_close /
                             df_data.ltc_close.shift(1)) - 1
    df_data['nasdaq_return'] = (df_data.nasdaq_close /
                                df_data.nasdaq_close.shift(1)) - 1

    return df_data
