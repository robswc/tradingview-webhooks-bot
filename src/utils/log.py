

import logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger()

# FILE_HANDLER = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
# FILE_HANDLER.setFormatter(logFormatter)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(logFormatter)
