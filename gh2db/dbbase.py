from __future__ import print_function
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from sqlalchemy_utils import database_exists, create_database


class BaseEngine(object):
    def __init__(self):
        url = '{}://{}:{}@{}:{}/{}'.format(
            os.environ['DB_DIALECT'],
            os.environ['DB_USERNAME'],
            os.environ['DB_PASSWORD'],
            os.environ['DB_HOSTNAME'],
            os.environ['DB_PORT'],
            os.environ['DB_NAME']
        )

        echo_type = True
        if os.environ['DB_ECHO_TYPE'] == '1':
            echo_type = True

        engine = create_engine(url, echo=echo_type)
        if not database_exists(engine.url):
            create_database(engine.url)

        self.engine = engine


class BaseSession(BaseEngine):
    def __init__(self):
        super().__init__()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
