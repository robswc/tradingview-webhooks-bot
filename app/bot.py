import datetime
import uuid

from actions.utils.action_manager import am
from events.utils.event_manager import em
import actions.utils._loader as action_loader
import events.utils._loader as event_loader
from logger import create_logger

# create logger
log = create_logger('webhooksbot', 'logs')

# load events and actions
action_loader.load()
event_loader.load()


class WebhooksBot:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.event_log = []
        self.events = em.events
        log.info('Started webhooks bot')

    def add_event_log(self, event):
        """
        Adds unique date, event pair to event log.
        :param event: event to log.
        :return: void
        """
        hash = str(uuid.uuid4()).split('-')[0]
        log_event = {'timestamp': datetime.datetime.now(), 'event': event}
        self.event_log.append(log_event)

    def load_json(self, data):
        """
        Reads webhook data and executes accordingly.
        :param data: webhook JSON data.
        :return: confirmation.
        """
        if data['key'] is None:
            log.error('Webhook data does not contain a "key".')
            return False

        try:
            self.trigger_key(data['key'], data)
        except Exception as e:
            log.error(e)

    def trigger_key(self, key, data):
        """
        Triggers an event, given a key.
        :param key: key of event.
        :return: confirmation of event trigger.
        """
        try:
            event = em.get_event_by_key(key)
            event.trigger(data)
            self.add_event_log(event)
        except Exception as e:
            log.error(e)


# create bot
bot = WebhooksBot()

