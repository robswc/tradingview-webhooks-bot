"""
WARNING: DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING!
IF YOU WISH TO CREATE CUSTOM EVENTS, YOU MUST EITHER USE
THE INTERFACE (COMING SOON) OR CREATE NEW .PY FILES.
"""
import time
import uuid

from logger import create_logger


class Event:
    def __init__(self, name):
        self.name = name
        self.actions = []
        self.confirmation = True
        self.confirmation_queue = {}
        self.triggers = []
        self.trigger_log = []
        self.key = str(uuid.uuid4()).split('-')[0]
        self.log = create_logger(self.name, 'logs')

    def get_log(self):
        """
        Gets log file.
        :return: string
        """
        with open('logs/{}.log'.format(self.name)) as f:
            lines = f.read().splitlines()
        return lines

    def format_trigger_log(self):
        """
        Formats the trigger log.
        """
        if not self.trigger_log:
            return None

        tables = [{'headers': list(self.trigger_log[0].keys()), 'rows': []}]
        table_idx = 0

        for idx, row in enumerate(self.trigger_log):
            table = tables[table_idx]
            if list(row.keys()) == table.get('headers'):
                table.get('rows').append(list(row.values()))
            else:
                tables.append({'headers': list(self.trigger_log[0].keys()), 'rows': []})
                table_idx = table_idx + 1

        return tables

    def add_confirmation(self, tid, data):
        """
        Adds trigger to confirmation queue.
        :param tid: trigger id
        :param data: data for run
        """
        self.log.info('{} added trigger to confirmation queue with id "{}".'.format(self.name, tid))
        self.confirmation_queue.update({tid: data})

    def confirm(self, tid):
        """
        Confirms (runs) a trigger from the confirmation queue, based off the trigger id.
        :param tid: trigger id.
        """
        self.log.info('"{}" confirmed'.format(tid))
        data = self.confirmation_queue.get(tid)
        self.run_actions(data)

    def reject(self, tid):
        """
        Rejects a trigger and deletes it from the confirmation queue, based off id.
        :param tid: trigger id
        """
        self.confirmation_queue.pop(tid)
        self.log.info('"{}" rejected'.format(tid))

    def run_actions(self, data):
        # triggers the run of all actions within the event.
        for action in self.actions:
            self.log.info(action.log_run(data))

    def trigger(self, data):
        """
        Method to trigger event.  Causes all event's actions to be executed.
        :param data: data for event/action
        :return: void
        """
        # log trigger event
        self.log.info('{} triggered'.format(self.name))
        self.trigger_log.append(data)
        # handle confirmation
        if self.confirmation:
            # create unique id for trigger
            tid = str(uuid.uuid4()).split('-')[0]
            data.update({'tid': tid})
            print(data)
            if self.confirmation:
                self.add_confirmation(tid, data)
                return {'success': True, 'trigger_id': tid}
            else:
                self.run_actions(data)
                return {'success': True}
