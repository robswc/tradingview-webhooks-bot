import datetime
from actions.utils.action import Action
from actions.utils.action_manager import am  # !IMPORTANT


class LogEvent(Action):
    def __init__(self, name):
        """
        Initializer, inherits from Action class.
        :param name: Name of your action.
        """
        Action.__init__(self, name)
        self.name = 'LogEvent'

    def run(self, data):
        """
        The run method, put main logic here.
        :param data: optional, any required data.
        :return: confirmation of completed action.
        """
        # run logic here
        return {'Status': 'OK'}


"""
Register the action with the action manager (am), so it can be used by events.
"""
am.register(LogEvent('LogEvent'))
