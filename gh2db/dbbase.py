from __future__ import print_function

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .logger import get_module_logger, handle_db_logger

handle_db_logger()
logger = get_module_logger(__name__)


class BaseEngine(object):
    def __init__(self):
        url = os.environ.get('GH2DB_DB_URI', 'mysql://root:@localhost:22/gh2db?charset=utf8')
        logger.debug(f'GH2DB_DB_URI: {url}')
        engine = create_engine(url, echo=False)
        self.engine = engine


class BaseSession(BaseEngine):
    def __init__(self):
        super().__init__()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
