import asyncio
import ccxt.async_support as ccxtasync
import ast, os, time, sys, ccxt
from dotenv import load_dotenv
from core.exchange import CryptoExchange
from core.trade import TradeExecutor
from core.talib import TechnicalAnalysis
from pprint import pprint
from loguru import logger


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
    #pprint(exchange.fetch_orders())

    bid = exchange.fetch_bid(data['symbol'])
    ask = exchange.fetch_ask(data['symbol'])
    orderSizes = exchange.fetch_orderSizes(data['symbol'])
    bidSize = orderSizes['bids'][0][1]
    askSize = orderSizes['asks'][0][1]
    buyLopsided = (bidSize / 2) > askSize
    sellLopsided = (askSize / 2) > bidSize
    if side == 'buy':
        if buyLopsided:
            order_price = ask + 5.0
            logger.warning("Heavily buy-sided. Executing market order @ {}. {} | {}.", order_price, bidSize, askSize)
        else:
            order_price = bid
        return order_price
    elif side == 'sell':
        if sellLopsided:
            order_price = bid - 5.0
            logger.warning("Heavily sell-sided. Executing market order @ {}. {} | {}.", order_price, bidSize, askSize)
        else:
            order_price = ask
        return order_price
    logger.info('Limit Order Set at {}', order_price)

def send_order(data):
    side = data['side']
    order_price = pre_processing(data)
    params = {'text': data['algo']}
    try:
        if side == 'buy':
            order = exchange.create_buy_order(data['symbol'], os.getenv("QTY"), order_price, params )
        elif side == 'sell':
            order = exchange.create_sell_order(data['symbol'], os.getenv("QTY"), order_price, params )
        post_processing(data, order)
    except Exception as err:
        logger.critical("An error occured while attempting to post order. | {}", err)


def post_processing(data, order):
    orderID = order['id']
    originalPrice = order['price']
    x = 0
    while x < 30:
        checkOrder = exchange.fetch_order(orderID)
        orderFilled = (checkOrder['filled'])
        orderRemaining = (checkOrder['remaining'])
        orderStatus = (checkOrder['status'])
        orderPrice = checkOrder['price']
        logger.log("ORDER", 'Price: {} | Order Filled: {} | Order Remaining: {}, Status: {}', orderPrice, orderFilled, orderRemaining, orderStatus)
        if orderStatus == 'closed' and orderRemaining == 0.0:
            logger.success("Order successfully filled.")
            x = 30
        else:

            time.sleep(0.25)
            #pprint(exchange.fetch_open_orders())
            bid = exchange.fetch_bid(data['symbol'])
            ask = exchange.fetch_ask(data['symbol'])
            #logger.info('Bid: {} | Ask: {}', bid, ask)
            if (data['side'] == 'buy') and orderPrice != bid and order['remaining'] > 0:
                logger.warning('Attempting to Re-Adjust Limit Price to {}', bid)
                params = {'text' : 'Buy limit order readjustment...'}
                try:
                    newOrder = exchange.create_buy_order(data['symbol'], os.getenv("QTY"), bid, params )
                    cancelOrder = exchange.cancel_order(orderID)
                    orderID = newOrder['id']
                except:
                    logger.critical('Error while attempting to readjust buy limit order.')

            elif (data['side'] == 'sell') and orderPrice != ask and order['remaining'] > 0:
                logger.info('Attempting to Re-Adjust Limit Price to {}', ask)
                params = {'text' : 'Sell limit order readjustment...'}
                try:
                    newOrder = exchange.create_sell_order(data['symbol'], os.getenv("QTY"), ask, params )
                    cancelOrder = exchange.cancel_order(orderID)
                    orderID = newOrder['id']
                except:
                    logger.critical('Error while attempting to readjust sell limit order.')
            x += 1

    if x >= 30 and orderStatus != 'closed':
        pass
        #cancelorder and do marketbuy
    #print(order)
    #print('Setting Entry Stop At: ', calc_entry_stop(data['side'], calc_price(order['price'])))
    free_balance = (exchange.free_balance['BTC'])
    open_orders = exchange.fetch_open_orders()
    current_position = exchange.get_position()
    logger.info('Avail. Balance: {} BTC | Curr. Position Size: {} | Avg. Position Entry: {} | Open Orders: {}', free_balance, current_position[0]['currentQty'], current_position[0]['avgEntryPrice'], len(open_orders))


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
ccxt_async = getattr(ccxt, exchange_id)({
    'urls':{
        'api':'https://testnet.bitmex.com'
    },
    'apiKey': exchange_key,
    'secret': exchange_secret,
    'verbose': False,
    'enableRateLimit': True,
})

exchange = CryptoExchange(ccxt_ex)
#exchangeAsync = AsyncExchange(ccxt_async)
trade = TradeExecutor(exchange)
