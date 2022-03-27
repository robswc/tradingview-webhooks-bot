# configure logging
from logging import getLogger, DEBUG

from utils.log import CONSOLE_HANDLER

logger = getLogger(__name__)
logger.addHandler(CONSOLE_HANDLER)
logger.setLevel(DEBUG)


class Event:
    def __init__(self):
        self.name = 'Unnamed Event'
        self._actions = []
        self.logs = []

    def __str__(self):
        return f'{self.name}'

    def register_action(self, action):
        """
        Will implement checking here eventually (tm)
        :param action: Action() to register
        """
        self._actions.append(action)

    def trigger_actions(self):
        logger.info(f'EVENT TRIGGERED --->\t{str(self)}')
        for action in self._actions:
            action.run()
