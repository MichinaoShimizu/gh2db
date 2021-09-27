from __future__ import print_function

import os
import sys
from logging import StreamHandler, getLogger

import coloredlogs


def handle_db_logger():
    logger = getLogger('sqlalchemy.engine')
    logger.addHandler(StreamHandler(sys.stderr))
    logger.propagate = False
    coloredlogs.DEFAULT_LOG_FORMAT = '[%(asctime)s %(levelname)s] %(message)s'
    coloredlogs.install(level=os.environ.get('GH2DB_DB_LOG_LEVEL', 'ERROR'), logger=logger)


def get_module_logger(module):
    logger = getLogger(module)
    logger.addHandler(StreamHandler(sys.stderr))
    logger.propagate = False
    coloredlogs.DEFAULT_LOG_FORMAT = '[%(asctime)s %(levelname)s] %(message)s'
    coloredlogs.install(level=os.environ.get('GH2DB_APP_LOG_LEVEL', 'INFO'), logger=logger)
    return logger
