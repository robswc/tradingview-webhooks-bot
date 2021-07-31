"""
WARNING: DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING!
IF YOU WISH TO CREATE CUSTOM ACTIONS, YOU MUST EITHER USE
THE INTERFACE (COMING SOON) OR CREATE NEW .PY FILES.
"""

from logger import create_logger
log = create_logger('action', 'logs')


class Action:
    """
    Action class template.
    """

    def __init__(self, name):
        self.name = name

    def log_run(self, data):
        """
        Logs a action run.
        :param data: data for action run
        :return:
        """
        log.info('{} running...'.format(self.name))
        result = self.run(data)
        log.info('{} finished running'.format(self.name))
        return result

    def run(self, data):
        pass
