# Python

# Pyscopg2
import psycopg2

# SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


try:
    # Connect to the database
    
    SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL']

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    Base = declarative_base()
    
    #meta = MetaData

    #conn = engine.connect()
    
    
    print("Connection to database successful")
    
except Exception as ex:
    print(ex)

