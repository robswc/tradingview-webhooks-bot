import datetime
from logging import getLogger, DEBUG

from utils.log import CONSOLE_HANDLER

logger = getLogger(__name__)
logger.addHandler(CONSOLE_HANDLER)
logger.setLevel(DEBUG)


class ActionManager:
    def __init__(self):
        self._actions = []

    def get(self, action_name: str):
        """
        Gets action from manager that matches given name
        :param action_name: name of action
        :return: Action()
        """
        for action in self._actions:
            if action.name == action_name:
                return action

        raise ValueError(f'Cannot find action with name {action_name}')


am = ActionManager()


class ActionLogEvent:
    def __init__(self, status, msg):
        self.timestamp = datetime.datetime.now()
        self.status = status
        self.msg = msg


class Action:
    objects = am

    def __init__(self):
        self.name = 'Unnamed Action'
        self.logs = []

    def __str__(self):
        return f'{self.name}'

    def get_logs(self):
        """
        Gets run logs in descending order
        :return: list
        """
        return self.logs

    def run(self, *args, **kwargs):
        """
        Runs, logs action
        """
        self.logs.append(ActionLogEvent('INFO', 'action run'))
        logger.info(f'ACTION TRIGGERED --->\t{str(self)}')
        pass
