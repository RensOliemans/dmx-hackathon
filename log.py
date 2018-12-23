import logging

from config import LOGLVL


def get_logger(name):
    logging.basicConfig(level=LOGLVL)
    return logging.getLogger(name)
