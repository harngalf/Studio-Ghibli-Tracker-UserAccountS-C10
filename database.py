
# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker




try:
    # Connect to the database
    
    #SQLALCHEMY_DATABASE_URL = "postgresql://harngalf:A142536@postgres/std_ghibli_db"
    #SQLALCHEMY_DATABASE_URL = "postgresql://harngalf:A142536@localhost:5432/std_ghibli_db"
    #DATABASE_URL = "postgresql://harngalf:A142536@localhost:5432/std_ghibli_db"
    DATABASE_URL = 'postgres://yayrtajuzkmisy:781072834cdacb0f7e4b63106f0b84907ba9ed57076a8f99876be2db1f8d98d7@ec2-34-194-73-236.compute-1.amazonaws.com:5432/dan4kvev3lephd'

    #database = databases.Database(DATABASE_URL)

    #metadata = sqlalchemy.MetaData()

    #conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    engine = create_engine(
        #SQLALCHEMY_DATABASE_URL
        DATABASE_URL
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    Base = declarative_base()
    #metadata.create_all(engine)
    
    #meta = MetaData

    #conn = engine.connect()
    
    
    print("Connection to database successful")
    
except Exception as ex:
    print(ex)

