import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.transactions as trans
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.accounts as accounts


def save_tick_data(tick_data, mid_price_list):
    mid_price = (float(tick_data['bids'][0]['price']) +
                 float(tick_data['asks'][0]['price'])) / 2
    mid_price_list.append(mid_price)
    return mid_price_list


def get_open_positions(client, account_id, instrument):
    try:
        position_data = positions.PositionDetails(account_id, instrument)
        position_data = client.request(position_data)
        position = float(position_data['position']['long']['units']) + \
                   float(position_data['position']['short']['units'])
        print("Position: " + str(position) + " " + instrument)
    except Exception:
        position = 0
        print("Position: " + str(position) + " " + instrument)
    return position


def get_trade_details(client, account_id, instrument):
    # Get last trade id
    trades_data = trades.TradesList(account_id, instrument)
    trades_data = client.request(trades_data)
    last_trade_id = trades_data['lastTransactionID']
    # Get last trade details
    trans_data = trans.TransactionDetails(account_id, last_trade_id)
    trans_data = client.request(trans_data)
    # Create variables
    instrument_traded = trans_data['transaction']['instrument']
    units_traded = trans_data['transaction']['units']
    price_traded = trans_data['transaction']['price']
    print("Traded " + units_traded + " " + instrument_traded +
          " at " + price_traded)


def submit_buy(client, account_id, trade_size, instrument):
    data = {
  "order": {
    "units": trade_size,
    "instrument": instrument,
    "timeInForce": "FOK",
    "type": "MARKET",
    "positionFill": "DEFAULT"
  }
}
    order_request = orders.OrderCreate(account_id, data)
    client.request(order_request)
    order_response = order_request.response


def submit_sell(client, account_id, trade_size, instrument):
    data = {
        "order": {
            "units": (-1 * trade_size),
            "instrument": instrument,
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
    }
    order_request = orders.OrderCreate(account_id, data)
    client.request(order_request)
    order_response = order_request.response


def get_nav(client, account_id):
    account_summary = accounts.AccountSummary(account_id)
    account_summary = client.request(account_summary)
    nav = float(account_summary['account']['NAV'])
    return nav
