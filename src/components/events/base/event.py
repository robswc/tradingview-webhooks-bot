# configure logging
from datetime import datetime
from hashlib import md5
from logging import getLogger, DEBUG

from commons import LOG_LOCATION, UNIQUE_KEY
from components.logs.log_event import LogEvent
from utils.log import get_logger

logger = get_logger(__name__)


class EventManager:
    def __init__(self):
        self._events = []

    def get_all(self):
        """
        Gets all events from manager
        :return: list of Event()
        """
        return self._events

    def get(self, event_name: str):
        """
        Gets event from manager that matches given name
        :param event_name: name of event
        :return: Event()
        """
        for event in self._events:
            if event.name == event_name:
                return event

        raise ValueError(f'Cannot find event with name {event_name}')


em = EventManager()


class Event:
    objects = em

    def __init__(self):
        self.name = self.get_name()
        self.webhook = True
        # generate consistent hash using hashlib, based off of name
        self.key = f'{self.name}:{md5(f"{self.name + UNIQUE_KEY}".encode()).hexdigest()[:6]}'
        self._actions = []
        self.logs = [LogEvent().from_line(line) for line in open(LOG_LOCATION, 'r') if line.split(',')[0] == self.name]

    def get_name(self):
        return type(self).__name__

    def add_action(self, action):
        self._actions.append(action)

    def register(self):
        self.objects._events.append(self)

    def __str__(self):
        return f'{self.name}'

    def get_last_log_time(self):
        return self.logs[-1].get_event_time()

    def register_action(self, action):
        """
        Will implement checking here eventually (tm)
        :param action: Action() to register
        """
        self._actions.append(action)

    def trigger(self, *args, **kwargs):
        # handle logging
        logger.info(f'EVENT TRIGGERED --->\t{str(self)}')
        log_event = LogEvent(self.name, 'triggered', datetime.now(), f'{self.name} was triggered')
        log_event.write()

        # pass data
        data = kwargs.get('data')

        self.logs.append(log_event)
        for action in self._actions:
            action.run(data=data)
