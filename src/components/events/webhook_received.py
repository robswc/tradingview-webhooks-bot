from components.events.base.event import Event


class WebhookReceived(Event):
    def __init__(self):
        super().__init__()
