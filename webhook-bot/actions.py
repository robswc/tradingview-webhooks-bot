import ccxt, ast, os, logging
from dotenv import load_dotenv
from core.exchange import CryptoExchange
from core.trade import TradeExecutor


def parse_webhook(webhook_data):

    """
    This function takes the string from tradingview and turns it into a python dict.
    :param webhook_data: POST data from tradingview, as a string.
    :return: Dictionary version of string.
    """

    data = ast.literal_eval(webhook_data)
    return data


def calc_price(given_price):

    """
    Will use this function to calculate the price for limit orders.
    :return: calculated limit price
    """

    if given_price == None:
        price = given_price
    else:
        price = given_price
    return price

def calc_entry_stop(side, price):
    if side == 'buy':
        stop = float(price) * (1.0 - float(os.getenv("ENTRY_STOP"))/100)
        return stop
    elif side == 'sell':
        stop = float(price) * (1.0 + float(os.getenv("ENTRY_STOP"))/100)
        return stop
    else:
        return 0


def process_alert(data):
    send_order(data)

def pre_processing(data):
    side = data['side']
    bid = exchange.fetch_bid(data['symbol'])
    ask = exchange.fetch_ask(data['symbol'])
    orderSizes = exchange.fetch_orderSizes(data['symbol'])
    bidSize = orderSizes['bids'][0][1]
    askSize = orderSizes['asks'][0][1]
    buyLopsided = (bidSize / 2 > askSize)
    sellLopsided = (askSize / 2 > bidSize)
    if side == 'buy':
        if buyLopsided:
            order_price = ask
            logging.info(f'Heavily buy-sided. Executing market order. {bidSize} | {askSize}.')
        else:
            order_price = bid
        return order_price
    elif side == 'sell':
        if sellLopsided:
            order_price = bid
            logging.info(f'Heavily sell-sided. Executing market order. {bidSize} | {askSize}.')
        else:
            order_price = ask
        return order_price
    logging.info(f'Limit Order Set at {order_price}')

def send_order(data):
    side = data['side']
    order_price = pre_processing(data)
    params = {'text':'Interceptor'}
    if side == 'buy':
        order = exchange.create_buy_order(data['symbol'], os.getenv("QTY"), order_price, params )
    elif side == 'sell':
        order = exchange.create_sell_order(data['symbol'], os.getenv("QTY"), order_price, params )
    print('Sending:', data['symbol'], data['type'], data['side'], os.getenv("QTY"))
    print('Setting Entry Stop At: ', calc_entry_stop(data['side'], calc_price(data['price'])))
    post_processing(order)

def post_processing(order):
    print(order)
    free_balance = (exchange.free_balance['BTC'])
    logging.info(f'Available Balance: {free_balance} BTC.')


load_dotenv(dotenv_path='config.env')
exchange_id = os.getenv("EXCHANGE")
exchange_key = os.getenv("EXCHANGE_API")
exchange_secret = os.getenv("EXCHANGE_SECRET")

ccxt_ex = getattr(ccxt, exchange_id)({
    'urls':{
        'api':'https://testnet.bitmex.com'
    },
    'apiKey': exchange_key,
    'secret': exchange_secret,
    'verbose': False,
    'enableRateLimit': True,
})


exchange = CryptoExchange(ccxt_ex)
trade = TradeExecutor(exchange)
