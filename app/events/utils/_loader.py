import importlib
from os import listdir
from os.path import isfile, join


def load():
    """
    Loads Events
    """
    event_files = [f for f in listdir('events') if isfile(join('events', f))]
    print('\nLoading events...')
    success = []
    failed = []
    for event in event_files:
        try:
            importlib.import_module('events.{}'.format(event[:-3]))
            print('Successfully loaded:\t{}'.format(event))
            success.append(event)
        except Exception as e:
            failed.append(event)
            print('Error loading {}!\n{}'.format(event, e))

    print('[{}/{}] events loaded successfully.\n'.format(len(success), len(success) + len(failed)))

