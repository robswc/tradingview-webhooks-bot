from shutil import copyfile


class ActionManager:
    def __init__(self):
        self.actions = []

    def register(self, action):
        """
        Registers action with the action manager, making it usable in events.
        :param action: action to register.
        :return: void
        """
        self.actions.append(action)
        print('Registered:\t{}'.format(action.name))

    def create_action(self, name, file_name):
        """
        Creates action, given name and file name.
        :param name: name of action
        :param file_name: name of file
        :return: void
        """
        try:
            copyfile('actions/utils/_template.py', 'actions/{}.py'.format(file_name))
            with open('actions/{}.py'.format(file_name), "r") as f:
                lines = f.readlines()
            with open('actions/{}.py'.format(file_name), "w") as f:
                for line in lines[0:3]:
                    f.write(line)
                for line in lines[7:]:
                    line = line.replace('Template', name)
                    f.write(line)
            print('Action "{}" created successfully! It can be found here: actions/{}.py'.format(name, file_name))
        except Exception as e:
            print(e)

    def get_action(self, name):
        """
        Gets action from action manager, based on action name.
        :param name: name of action
        :return: Action()
        """
        for a in self.actions:
            if a.name == name:
                return a


# creates the action manager
am = ActionManager()
