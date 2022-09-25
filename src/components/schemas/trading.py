import json

from components.schemas.base.schema import Schema


class Order(Schema):
    def __init__(self):
        super().__init__()
        self.order_type: str = 'market'
        self.side: str = 'buy'
        self.quantity: float = 0.0
        self.symbol: str = 'XBTUSD'
        self.price: float = 0.0

    def as_json(self):
        as_dict = {
            'order_type': self.order_type,
            'side': self.side,
            'quantity': self.quantity,
            'symbol': self.symbol,
            'price': self.price
        }
        return json.dumps(as_dict)

class Position(Schema):
    def __init__(self):
        super().__init__()
        self.symbol: str = 'XBTUSD'
        self.quantity: float = 0.0
        self.entry_price: float = 0.0
        self.take_profit: float = 0.0
        self.take_loss: float = 0.0

    def as_json(self):
        as_dict = {
            'symbol': self.symbol,
            'quantity': self.quantity,
            'entry_price': self.entry_price,
            'take_profit': self.take_profit,
            'take_loss': self.take_loss
        }
        return json.dumps(as_dict)
