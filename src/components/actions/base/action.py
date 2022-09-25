import datetime
from logging import getLogger, DEBUG

from components.logs.log_event import LogEvent
from utils.log import get_logger

logger = get_logger(__name__)


class ActionManager:
    def __init__(self):
        self._actions = []

    def get_all(self):
        """
        Gets all actions from manager
        :return: list of Action()
        """
        return self._actions

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
        self.name = self.get_name()
        self.logs = []

    def get_name(self):
        return type(self).__name__

    def __str__(self):
        return f'{self.name}'

    def get_logs(self):
        """
        Gets run logs in descending order
        :return: list
        """
        return self.logs

    def register(self):
        """
        Registers action with manager
        """
        self.objects._actions.append(self)
        logger.info(f'ACTION REGISTERED --->\t{str(self)}')

    def run(self, *args, **kwargs):
        """
        Runs, logs action
        """
        self.logs.append(ActionLogEvent('INFO', 'action run'))
        log_event = LogEvent(self.name, 'action_run', datetime.datetime.now(), f'{self.name} triggered')
        log_event.write()
        logger.info(f'ACTION TRIGGERED --->\t{str(self)}')
