from __future__ import print_function

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from .logger import get_module_logger, handle_db_logger

handle_db_logger()
logger = get_module_logger(__name__)


class BaseEngine(object):
    def __init__(self):
        url = '{}://{}:{}@{}:{}/{}'.format(
            os.environ.get('GH2DB_DB_DIALECT', 'mysql'),
            os.environ.get('GH2DB_DB_USERNAME', 'root'),
            os.environ.get('GH2DB_DB_PASSWORD', ''),
            os.environ.get('GH2DB_DB_HOSTNAME', 'localhost'),
            os.environ.get('GH2DB_DB_PORT', '22'),
            os.environ.get('GH2DB_DB_NAME', 'gh2db')
        )

        logger.debug(f'DB: {url}')

        engine = create_engine(url, echo=False)
        if not database_exists(engine.url):
            logger.info('Database is not exist.Try Create Database.')
            create_database(engine.url)
            logger.info('Database create complete.')

        self.engine = engine


class BaseSession(BaseEngine):
    def __init__(self):
        super().__init__()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
