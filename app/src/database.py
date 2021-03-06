# Python

# Pyscopg2
#from psycopg2 import psycopg2
#import databases


# SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import sqlalchemy



try:
    # Connect to the database
    
    SQLALCHEMY_DATABASE_URL = "postgresql://harngalf:A142536@postgres/std_ghibli_db"
    #SQLALCHEMY_DATABASE_URL = "postgresql://harngalf:A142536@localhost:5432/std_ghibli_db"
    #DATABASE_URL = "postgresql://harngalf:A142536@localhost:5432/std_ghibli_db"
    #DATABASE_URL = os.environ['DATABASE_URL']

    #database = databases.Database(DATABASE_URL)

    #metadata = sqlalchemy.MetaData()

    #conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
        #DATABASE_URL
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

