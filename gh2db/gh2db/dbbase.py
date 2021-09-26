from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


class BaseEngine(object):
    def __init__(self):
        load_dotenv()

        url = '{}://{}:{}@{}:{}/{}'.format(
            os.environ['DB_DIALECT'],
            os.environ['DB_USERNAME'],
            os.environ['DB_PASSWORD'],
            os.environ['DB_HOSTNAME'],
            os.environ['DB_PORT'],
            os.environ['DB_NAME']
        )

        echo_type = False
        if os.environ['DB_ECHO_TYPE'] == '1':
            echo_type = True

        self.engine = create_engine(url, echo=echo_type)


class BaseSession(BaseEngine):
    def __init__(self):
        super().__init__()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
