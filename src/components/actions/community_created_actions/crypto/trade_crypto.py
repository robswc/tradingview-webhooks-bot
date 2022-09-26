from components.actions.base.action import Action


class TradeCrypto(Action):
    def __init__(self):
        super().__init__()

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)
        """
        Custom run method. Add your custom logic here.
        """
        data = self.validate_data()
        print('Data from webhook:', data)
        print('Data is of type:', type(data))
        print('Looking for order symbol...')
        symbol = data.get('symbol', 'Not found :(')
        print('Symbol:', symbol)
        print('Looking for order type...')
        order_type = data.get('order_type', 'Not found :(')
        print('Order type is:', order_type)
        print('\n\nUse the data above to make your trade!')
        print('\nhttps://github.com/ccxt/ccxt#python-1')
        print('CCXT is an example of a library you can use to make trades.\n\n')