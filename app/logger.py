import logging


def create_logger(name, path):
    """
    Creates a logger
    :param name: name of logger.
    :param path: path to file output.
    :return: logger()
    """
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # format log path
    fh = logging.FileHandler('{}/{}.log'.format(path, name))

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add handlers
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger