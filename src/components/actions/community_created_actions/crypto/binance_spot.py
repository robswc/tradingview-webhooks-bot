from components.actions.base.action import Action
import ccxt as ccxt

class BinanceSpot(Action):
    #Add your API_KEY from Binance Testnet or Mainnet
    API_KEY = ''
    #Add your API_SECRET from Binance Testnet or Mainnet
    API_SECRET = ''

    exchange = ccxt.binance({
            'rateLimit': 2000,
            'enableRateLimit': True,
            'apiKey': API_KEY,
            'secret': API_SECRET,
            'id': 'binance',
        })

    def __init__(self):
        super().__init__()
        #uncomment the below line to use sandbox/testnet api
        # exchange = self.exchange.set_sandbox_mode(True)

    def place_order(self, symbol, side, price=None):
        try:

            # Get the balance of the base currency
            balance = self.exchange.fetch_balance()
            if side == 'buy':
                base_balance = balance['free'][symbol[-4:]]
            elif side == 'sell':
                base_balance = balance['free'][symbol[:-4]]
            
            # Calculate the amount of asset to buy or sell
            if side == 'buy':
                amount = base_balance / price
            elif side == 'sell':
                amount = base_balance

            markets = self.exchange.load_markets()
            formatted_amount = self.exchange.amount_to_precision(symbol, amount)
            order = self.exchange.create_market_order(symbol, side, quoteOrderQty=formatted_amount)
            print(order)
            # Print the order details
        except ccxt.BaseError as e:
            # Handle the exception
            print("An error occurred while placing the order:", e)
        except ValueError as e:
            # Handle the exception
            print("An error occurred while checking the filters or calculating the amount:", e)

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)  # this is required
        data = self.validate_data()
        self.place_order(symbol=data['symbol'], side=data['side'])
