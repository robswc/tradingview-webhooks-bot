import importlib
from os import listdir
from os.path import isfile, join


class DuplicateFileName(Exception):
    def __init__(self, name):
        self.message = '{} already exists!'.format(name)
        super().__init__(self.message)

    def __str__(self):
        return self.message


def load():
    """
    Loads actions
    """
    action_files = [f for f in listdir('actions') if isfile(join('actions', f))] + [f for f in
                                                                                    listdir('actions/builtins') if
                                                                                    isfile(join('actions/builtins', f))]
    print('\nLoading actions...')
    success = []
    failed = []
    name_list = []
    for action in action_files:
        if action in name_list:
            raise DuplicateFileName(name=action)
        else:
            name_list.append(action)
        try:
            importlib.import_module('actions.{}'.format(action[:-3]))
            print('Successfully loaded:\t{}'.format(action))
            success.append(action)
        except Exception as e:
            try:
                importlib.import_module('actions.builtins.{}'.format(action[:-3]))
                print('Successfully loaded:\t{}'.format(action))
                success.append(action)
            except Exception as e:
                failed.append(action)
                print('Error loading {}!\n{}'.format(action, e))

    print('[{}/{}] actions loaded successfully.\n'.format(len(success), len(success) + len(failed)))
