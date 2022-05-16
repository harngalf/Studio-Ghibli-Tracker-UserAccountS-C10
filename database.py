
# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# #SQLALCHEMY_DATABASE_URL = "postgresql://harngalf:A142536@postgres/std_ghibli_db"
# SQLALCHEMY_DATABASE_URL = "postgresql://harngalf:A142536@localhost:5432/std_ghibli_db"
# # #
# # SQLALCHEMY_DATABASE_URL = "postgresql://yayrtajuzkmisy:781072834cdacb0f7e4b63106f0b84907ba9ed57076a8f99876be2db1f8d98d7@ec2-34-194-73-236.compute-1.amazonaws.com:5432/dan4kvev3lephd"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
#     #DATABASE_URL
#     )

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
#     )
# Base = declarative_base()

    

try:
    # Connect to the database
    
    SQLALCHEMY_DATABASE_URL = "postgresql://harngalf:A142536@localhost:5432/std_ghibli_db"
    #SQLALCHEMY_DATABASE_URL = "postgresql://yayrtajuzkmisy:781072834cdacb0f7e4b63106f0b84907ba9ed57076a8f99876be2db1f8d98d7@ec2-34-194-73-236.compute-1.amazonaws.com:5432/dan4kvev3lephd"


    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    Base = declarative_base()
  
    
    print("Connection to database successful")
    
except Exception as ex:
    print(ex)

