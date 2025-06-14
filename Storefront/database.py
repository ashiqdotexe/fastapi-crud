from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import create_engine
from dotenv import load_dotenv
import os
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL_STOREFRONT")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()