import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

USERNAME = os.environ["DB_USERNAME"]
HOSTNAME = os.environ["DB_HOSTNAME"]
PASSWORD = os.environ["DB_PASSWORD"]
DATABASE = os.environ["DB_DATABASE"]
DIALECT = os.environ["DB_DIALECT"]
PORT = os.environ["DB_PORT"]

SQLALCHEMY_DATABASE_URL = f"{DIALECT}://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)  # Generate tables?


class ConnectionDatabase:
    def __init__(self):
        self.session = Session()
