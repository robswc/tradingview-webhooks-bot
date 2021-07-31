from events.utils.event_manager import em
from actions.utils.action_manager import am
from events.utils.event import Event

"""
This is a simple event, to be used as a template.
"""


class Template(Event):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        # add actions
        self.actions = []
        self.key = '__KEY__'


"""
Register event with event manager (em).
"""
em.register(Template('Template'))
