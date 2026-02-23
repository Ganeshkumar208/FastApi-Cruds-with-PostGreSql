from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql://postgres:ganeshpg208@localhost:5432/firstdb"
engine = create_engine(db_url)
session = sessionmaker(autocommit = False, autoflush = False, bind=engine)