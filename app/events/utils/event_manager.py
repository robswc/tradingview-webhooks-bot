import uuid
from shutil import copyfile
import fileinput


class EventManager:
    def __init__(self):
        self.events = []

    def register(self, event):
        """
        Registers event with event manager.
        :param event: event to register.
        :return: void
        """
        self.events.append(event)

    def create_event(self, name, file_name):
        """
        Creates event, given name and file name.
        :param name: name of event
        :param file_name: name of file
        :return: void
        """
        try:
            copyfile('events/utils/_template.py', 'events/{}.py'.format(file_name))
            with open('events/{}.py'.format(file_name), "r") as f:
                lines = f.readlines()
            with open('events/{}.py'.format(file_name), "w") as f:
                for line in lines[0:3]:
                    f.write(line)
                for line in lines[7:]:
                    line = line.replace('Template', name).replace('__KEY__', str(uuid.uuid4()).split('-')[0])
                    f.write(line)
            print('event "{}" created successfully! It can be found here: events/{}.py'.format(name, file_name))
        except Exception as e:
            print(e)

    def get_event(self, name):
        """
        Gets event from event manager, based on event name.
        :param name: name of event
        :return: event()
        """
        for e in self.events:
            if e.name == name:
                return e

    def get_event_by_key(self, key):
        """
        Gets event from event manager by key.
        :param key: key of event.
        :return: Event()
        """
        for e in self.events:
            if e.key == key:
                return e


# creates the event manager
em = EventManager()
