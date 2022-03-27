from components.schemas.schema import Schema


class Order(Schema):
    def __init__(self):
        super().__init__()
        self.order_type = str
        self.side = str
        self.quantity = int
        self.symbol = str
        self.price = float
