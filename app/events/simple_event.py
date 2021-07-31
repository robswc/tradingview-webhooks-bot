from events.utils.event_manager import em
from actions.utils.action_manager import am
from events.utils.event import Event


class SimpleEvent(Event):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        # add actions
        self.actions = []
        self.key = 'df04342b'


"""
Register event with event manager (em).
"""
em.register(SimpleEvent('SimpleEvent'))
