from datetime import datetime

from commons import LOG_LOCATION, LOG_LIMIT


class LogEvent:
    def __init__(self, parent=None, event_type=None, event_time=None, event_data=None):
        self.parent = parent
        self.event_type = event_type
        self.event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.event_data = event_data

    def __str__(self):
        return "Event Type: " + self.event_type + " Event Time: " + self.event_time + " Event Data: " + self.event_data

    def get_event_type(self):
        return self.event_type

    def get_event_time(self):
        return self.event_time

    def get_event_data(self):
        return self.event_data

    def set_event_type(self, event_type):
        self.event_type = event_type

    def set_event_time(self, event_time):
        self.event_time = event_time

    def set_event_data(self, event_data):
        self.event_data = event_data

    def to_line(self):
        return self.parent + "," + self.event_type + "," + self.event_time + "," + self.event_data + "\n"

    def as_json(self):
        return {
            "parent": self.parent,
            "event_type": self.event_type,
            "event_time": self.event_time,
            "event_data": self.event_data.strip()
        }

    def from_line(self, line):
        self.parent, self.event_type, self.event_time, self.event_data = line.split(',')
        self.event_time = datetime.strptime(self.event_time, "%Y-%m-%d %H:%M:%S")
        return self

    def write(self):
        rows = open(LOG_LOCATION, 'r').readlines()
        if len(rows) >= LOG_LIMIT:
            log_file = open(LOG_LOCATION, 'w')
            log_file.writelines(rows[1:])
        else:
            log_file = open(LOG_LOCATION, 'a')
        log_file.write(self.to_line())
        log_file.close()