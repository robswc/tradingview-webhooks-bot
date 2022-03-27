from components.events.base.event import Event


class TemplateEventClass(Event):
    def __init__(self):
        super().__init__()
        self.name = '_TemplateEvent_'


template_event = TemplateEventClass()