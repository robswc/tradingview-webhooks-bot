from ccxt import Exchange, OrderNotFound, async_support
import asyncio
import json


class CryptoExchange:

    def __init__(self, exchange: Exchange):
        self.exchange = exchange
        self.exchange.load_markets()

    @property
    def free_balance(self):
        balance = self.exchange.fetch_free_balance()
        # surprisingly there are balances with 0, so we need to filter these out
        return {k: v for k, v in balance.items() if v > 0}

    def fetch_ticker(self, symbol: str = None):
        return self.exchange.fetch_ticker(symbol)['last']

    def fetch_ask(self, symbol: str = None):
        return self.exchange.fetch_ticker(symbol)['ask']

    def fetch_orderSizes(self, symbol: str = None):
        #print(self.exchange.fetch_order_book(symbol, 1))
        return self.exchange.fetch_order_book(symbol, 1)

    def fetch_bid(self, symbol: str = None):
        return self.exchange.fetch_ticker(symbol)['bid']

    def fetch_open_orders(self, symbol: str = None):
        return self.exchange.fetch_open_orders(symbol=symbol)

    def fetch_orders(self):
        return self.exchange.fetch_orders(limit=3)

    def fetch_order(self, order_id: int):
        return self.exchange.fetch_order(order_id)

    def edit_order(self, order_id: int, type: str, side: str, params: dict):
        return self.exchange.edit_order(order_id, type, side, params)

    def set_leverage(self, leverage: int):
        return self.exchange.privatePostPositionLeverage()

    def get_position(self):
        return self.exchange.privateGetPosition()

    def close_position(self, symbol: str, type: str, amount: float, price: float, params: dict):
        return self.exchange.create_order(symbol=symbol, type="limit", side="sell", amount=amount, price=price, params=params)

    def close_open_orders(self):
        try:
            self.exchange.privateDeleteOrderAll()
        except:
            # treat as success
            pass

    def cancel_order(self, order_id: int):
        try:
            self.exchange.cancel_order(order_id)
        except OrderNotFound:
            # treat as success
            pass

    def set_stoploss(self, symbol:str, amount: float, price: float, params: dict, side: str):
        return self.exchange.create_order(symbol=symbol, type="StopLimit", side=side, amount=amount, price=price, params=params)

    def create_sell_order(self, symbol: str, amount: float, price: float, params: dict):
        return self.exchange.create_order(symbol=symbol, type="limit", side="sell", amount=amount, price=price, params=params)

    def create_buy_order(self, symbol: str, amount: float, price: float, params: dict):
        return self.exchange.create_order(symbol=symbol, type="limit", side="buy", amount=amount, price=price, params=params)
