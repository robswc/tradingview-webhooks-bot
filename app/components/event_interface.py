import dash_html_components as html

from components.event_tile import EventTile

class EventInterface:
    def __init__(self):
        self.events = []

    def get(self, name):
        """
        Gets event from events list, given name.
        :param name: name of event
        :return: event
        """
        for e in self.events:
            if e.name == name:
                return e

    def render_event_log(self):
        """
        Renders event log.
        :return: html.Div()
        """

    def render_events(self):
        """
        Renders event tiles, returns html List.
        :return: html.Div()
        """
        # create event list
        event_list = []
        for event in self.events:
            event_list.append(EventTile(event).render())

        return html.Div(
            children=event_list,
            className='tile-container'
        )

# create event interface
ei = EventInterface()
