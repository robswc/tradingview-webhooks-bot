import asyncio
import logging

from ccxt import ExchangeError

# Future Implementation of Asynchronous Python

class TradeExecutor:

    def __init__(self, exchange, check_timeout: int = 15):
        self.check_timeout = check_timeout
        self.exchange = exchange

    async def execute_trade(self, trade):
        if isinstance(trade, ShortTrade):
            await self.execute_short_trade(trade)
        elif isinstance(trade, LongTrade):
            await self.execute_long_trade(trade)

    async def execute_short_trade(self, trade):
        sell_price = trade.start_price
        buy_price = trade.exit_price
        symbol = trade.exchange_symbol
        amount = trade.amount

        order = self.exchange.create_sell_order(symbol, amount, sell_price)
        logging.info(f'Opened sell order: {amount} of {symbol}. Target sell {sell_price}, buy price {buy_price}')

        await self._wait_order_complete(order['id'])

        # post buy order
        order = self.exchange.create_buy_order(symbol, amount, buy_price)

        await self._wait_order_complete(order['id'])
        logging.info(f'Completed short trade: {amount} of {symbol}. Sold at {sell_price} and bought at {buy_price}')

    async def execute_long_trade(self, trade):
        buy_price = trade.start_price
        #sell_price = trade.exit_price
        symbol = trade.exchange_symbol
        amount = trade.amount

        order = self.exchange.create_buy_order(symbol, amount, buy_price)
        logging.info(f'Opened long trade: {amount} of {symbol}. Target buy {buy_price}')

        await self._wait_order_complete(order.id)

        # post sell order
        #order = self.exchange.create_sell_order(symbol, amount, sell_price)

        #await self._wait_order_complete(order.id)
        logging.info(f'Completed long trade: {amount} of {symbol}. Bought at {buy_price}')

    async def _wait_order_complete(self, order_id):
        status = 'open'
        while status is 'open':
            await asyncio.sleep(self.check_timeout)
            order = self.exchange.fetch_order(order_id)
            status = order['status']

        logging.info(f'Finished order {order_id} with {status} status')

        # do not proceed further if we canceled order
        if status == 'canceled':
            raise ExchangeError('Trade has been canceled')
