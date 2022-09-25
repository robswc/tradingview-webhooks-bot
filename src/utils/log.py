import logging


def get_logger(name, level=logging.DEBUG):
    fmt = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    logger.setLevel(level)
    return logger
