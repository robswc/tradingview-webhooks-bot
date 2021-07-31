import datetime

import requests

from actions.utils.action import Action
from actions.utils.action_manager import am  # !IMPORTANT


class SimpleAction(Action):
    def __init__(self, name):
        """
        Initializer, inherits from Action class.
        :param name: Name of your action.
        """
        Action.__init__(self, name)
        self.name = 'SimpleAction'

    def run(self, data):
        """
        The run method, put main logic here.
        :param data: optional, any required data.
        :return: confirmation of completed action.
        """
        # run logic here
        print('This is a sample action, being executed!')
        print('This action will get quotes from bitmex.\nHowever, you can make it do whatever you want!')

        # use requests to get bitmex pricing data
        r = requests.get('https://www.bitmex.com/api/v1/quote',
                         params={'symbol': data.get('symbol'), 'count': 1}).json()
        print(r)

        # recommended to return some sort of status, as confirmation.
        return {'Status': 'OK', data.get('symbol'): r[0].get('bidPrice')}


"""
Register the action with the action manager (am), so it can be used by events.
"""
am.register(SimpleAction('SimpleAction'))
