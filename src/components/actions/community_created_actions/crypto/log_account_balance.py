import datetime
import random

from components.actions.base.action import Action
from components.logs.log_event import LogEvent


class LogAccountBalance(Action):
    def __init__(self):
        super().__init__()

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)  # this is required
        """
        Custom run method. Add your custom logic here.
        """
        data = self.validate_data()
        print('Data from webhook:', data)
        message = f'Account Balance is: ${random.randint(0, 100)} USD'
        timestamp = datetime.datetime.now()
        log = LogEvent(self.name, 'account_balance', timestamp, message)
        log.write()  # remember to write the log!

        # kraken = ccxt.kraken({
        #     'apiKey': 'YOUR_PUBLIC_API_KEY',
        #     'secret': 'YOUR_SECRET_PRIVATE_KEY',
        # })

        # kraken.load_markets()
        # print(kraken.fetch_balance())
