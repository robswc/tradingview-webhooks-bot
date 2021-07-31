from events.utils.event_manager import em
from actions.utils.action_manager import am
from events.utils.event import Event


class MyEvent(Event):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.confirmation = 5
        # add actions
        self.actions = [am.get_action('SimpleAction')]
        self.key = 'bf432902'


"""
Register event with event manager (em).
"""
em.register(MyEvent('MyEvent'))
