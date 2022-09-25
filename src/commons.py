# settings
import uuid

LOG_LOCATION = 'components/logs/log.log'
LOG_LIMIT = 100

# ensure log file exists
try:
    open(LOG_LOCATION, 'r')
except FileNotFoundError:
    open(LOG_LOCATION, 'w').close()

# DO NOT CHANGE
VERSION_NUMBER = '0.5'


# if key file exists, read key, else generate key and write to file
# WARNING: DO NOT CHANGE KEY ONCE GENERATED (this will break all existing events)
try:
    with open('.key', 'r') as key_file:
        UNIQUE_KEY = key_file.read().strip()
except FileNotFoundError:
    UNIQUE_KEY = uuid.uuid4()
    with open('.key', 'w') as key_file:
        key_file.write(str(UNIQUE_KEY))
        key_file.close()
