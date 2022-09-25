# settings
LOG_LOCATION = 'components/logs/log.log'
LOG_LIMIT = 100

# ensure log file exists
try:
    open(LOG_LOCATION, 'r')
except FileNotFoundError:
    open(LOG_LOCATION, 'w').close()

# DO NOT CHANGE
VERSION_NUMBER = '0.5'
