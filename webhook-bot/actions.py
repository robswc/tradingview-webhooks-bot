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

    data = ast.literal_eval(webhook_data)
    return data

def calc_price(given_price):

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
def set_entry_stop(symbol, amount, price, side):
    stopPrice = calc_entry_stop(side, price)
    params = {'stopPx' : int(price)}
    try:
        logger.log("ORDER", "Attempting to set stop-limit at {} for {} contracts.", price, amount)
        entryStop = exchange.set_stoploss(symbol, amount, int(stopPrice), params, side)
        logger.success("Stop-Limit set to {} for {} contracts.", price, amount)
    except Exception as err:
        logger.critical("Entry Stop could not be set. Msg: {}", err)
def get_acctstatus():
    current_price = exchange.fetch_ticker(os.getenv("MARKET"))
    current_position = exchange.get_position()
    #pprint(current_position)
    currentPos = current_position[0]['currentQty']
    if currentPos > 0:
        logger.opt(ansi=True).log("STATUS", "{} Price: <b>{}</b> | Pos. Size: <b><lg>Long {}</lg></b> | Entry: <b>{}</b> | ROE: {}% | PNL: {} {}", os.getenv("MARKET"), current_price, currentPos, current_position[0]['avgEntryPrice'], current_position[0]['unrealisedRoePcnt']*100, current_position[0]['unrealisedPnl']/10**8, current_position[0]['underlying'])
    elif currentPos < 0:
        logger.opt(ansi=True).log("STATUS", "{} Price: <b>{}</b> | Position: <b><lr>Short {}</lr></b> | Entry: <b>{}</b> | ROE: {}% | PNL: {} {}", os.getenv("MARKET"), current_price, currentPos, current_position[0]['avgEntryPrice'], current_position[0]['unrealisedRoePcnt']*100, current_position[0]['unrealisedPnl']/10**8, current_position[0]['underlying'])
    else:
        logger.warning("Currently not in a position. Awaiting next order.")


def process_alert(data):
    send_order(data)

def pre_processing(data):
    exchange.close_open_orders()
    side = data['side']
    current_position = exchange.get_position()
    position_size = current_position[0]['currentQty']
    if position_size == 0: orderQTY = os.getenv("QTY")
    if position_size != 0: orderQTY = abs(position_size * 2)
    #pprint(exchange.fetch_orders())
    #closePosition = exchange.close_position()
    bid = exchange.fetch_bid(data['symbol'])
    ask = exchange.fetch_ask(data['symbol'])
    orderSizes = exchange.fetch_orderSizes(data['symbol'])
    bidSize = orderSizes['bids'][0][1]
    askSize = orderSizes['asks'][0][1]
    buyLopsided = (bidSize / 2.5) > askSize
    sellLopsided = (askSize / 2.5) > bidSize
    if side == 'buy' and position_size <= 0:
        if buyLopsided:
            order_price = ask + 5.0
            logger.warning("Heavily buy-sided. Executing market order @ {}. {} | No. of Contracts: {}.", order_price, bidSize, orderQTY)
        else:
            order_price = bid
        return [order_price, orderQTY]
    elif side == 'sell' and position_size >= 0:
        if sellLopsided:
            order_price = bid - 5.0
            logger.warning("Heavily sell-sided. Executing market order @ {}. {} | No. of Contracts: {}.", order_price, bidSize, orderQTY)
        else:
            order_price = ask
        return [order_price, orderQTY]
    else:
        logger.critical("Error: Buy side is incorrect or there was an error somewhere.")
        return [0, 0]

def send_order(data):
    side = data['side']
    pre_processing_results = pre_processing(data)
    order_price = pre_processing_results[0]
    order_quantity = pre_processing_results[1]
    params = {'text': data['algo']}
    try:
        if side == 'buy':
            order = exchange.create_buy_order(data['symbol'], order_quantity, order_price, params )
        elif side == 'sell':
            order = exchange.create_sell_order(data['symbol'], order_quantity, order_price, params )
        post_processing(data, order)
    except Exception as err:
        logger.critical("An error occured while attempting to post order. | {}", err)

def post_processing(data, order):
    current_position = exchange.get_position()
    orderID = order['id']
    originalPrice = order['price']
    position_size = current_position[0]['currentQty']
    if position_size == 0: orderQTY = os.getenv("QTY")
    if position_size != 0: orderQTY = abs(position_size * 2)
    avg_entry = current_position[0]['avgEntryPrice']
    x = 0
    while x < 30:
        checkOrder = exchange.fetch_order(orderID)
        orderFilled = (checkOrder['filled'])
        orderRemaining = (checkOrder['remaining'])
        orderStatus = (checkOrder['status'])
        orderPrice = checkOrder['price']
        logger.opt(ansi=True).log("ORDER", 'Price: {} | Order Filled: {} | Order Remaining: <b>{}</b> | Status: <b>{}</b>', orderPrice, orderFilled, orderRemaining, orderStatus)
        if orderStatus == 'closed' and orderRemaining == 0.0:
            logger.success("Order successfully filled.")
            x = 50
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
                    if (bid - originalPrice > float(os.getenv("SLIPPAGE_ALLOWED"))): bid = bid + 20.0

                    newOrder = exchange.create_buy_order(data['symbol'], orderQTY, bid, params )
                    cancelOrder = exchange.cancel_order(orderID)
                    orderID = newOrder['id']
                    if newOrder['status'] == "closed":
                        logger.log("ORDER", "New order successfully executed.")
                except Exception as err:
                    logger.critical('Error while attempting to readjust buy limit order. {}', err)

            elif (data['side'] == 'sell') and orderPrice != ask and order['remaining'] > 0:
                logger.info('Attempting to Re-Adjust Limit Price to {}', ask)
                params = {'text' : 'Sell limit order readjustment...'}
                try:
                    if (originalPrice - ask > float(os.getenv("SLIPPAGE_ALLOWED"))): ask = ask - 20.0
                    newOrder = exchange.create_sell_order(data['symbol'], orderQTY, ask, params )
                    cancelOrder = exchange.cancel_order(orderID)
                    orderID = newOrder['id']
                    if newOrder['status'] == "closed":
                        logger.log("ORDER", "New order successfully executed.")
                except Exception as err:
                    logger.critical('Error while attempting to readjust sell limit order. {}', err)
            x += 1

    if x >= 30 and orderStatus != 'closed':
        try:
            cancelOrder = exchange.cancel_order(orderID)
            params = {'text' : 'Limit order to market order adjustment...'}
            if data['side'] == 'buy':
                bid = exchange.fetch_bid(data['symbol']) + 10.0
                newOrder = exchange.create_buy_order(data['symbol'], orderQTY, bid, params )
                logger.log("ORDER", "Market Order Submitted | Fill Price: {} | Status: {}", newOrder['price'], newOrder['status'])

            elif data['side'] == 'sell':
                ask = exchange.fetch_ask(data['symbol']) - 10.0
                newOrder = exchange.create_sell_order(data['symbol'], orderQTY, ask, params )
                logger.log("ORDER", "Market Order Submitted | Fill Price: {} | Status: {}", newOrder['price'], newOrder['status'])

            else:
                logger.critical("Error while abandoning limit order for market order. [1]")
        except:
            logger.critical("Error while abandoning limit order for market order. [2]")

        #cancelorder and do marketbuy
    #print(order)
    #print('Setting Entry Stop At: ', calc_entry_stop(data['side'], calc_price(order['price'])))
    #cancelOrder = exchange.cancel_order(orderID)
    free_balance = round(exchange.free_balance['BTC'], 6)
    open_orders = exchange.fetch_open_orders()
    current_position = exchange.get_position()
    position_size = current_position[0]['currentQty']
    avg_entry = current_position[0]['avgEntryPrice']
    if position_size > 0: stopPrice = calc_entry_stop('buy', avg_entry)
    if position_size < 0: stopPrice = calc_entry_stop('sell', avg_entry)
    stopParams = {'stopPx' : stopPrice}
    if position_size > 0: stopSide = 'sell'
    if position_size < 0: stopSide = 'buy'
    set_entry_stop(data['symbol'], abs(position_size), price=stopPrice, side=stopSide)


    #pprint(current_position)
    logger.info('Avail. Balance: {} BTC | Curr. Position Size: {} | Avg. Position Entry: {} | Open Orders: {}', free_balance, position_size, avg_entry, len(open_orders))


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
