from logging import getLogger, StreamHandler, DEBUG
import coloredlogs
import sys


def get_logger(module):
    logger = getLogger(module)
    logger.addHandler(StreamHandler(sys.stderr))
    logger.setLevel(DEBUG)
    logger.propagate = False
    coloredlogs.DEFAULT_LOG_FORMAT = '[%(asctime)s %(levelname)s %(name)s:%(lineno)s] %(message)s'
    coloredlogs.install(level='DEBUG', logger=logger)

    return logger
