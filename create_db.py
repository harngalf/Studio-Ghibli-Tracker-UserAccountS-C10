
import database
import models 

Base = database.Base
engine = database.engine

print("creating database")

Base.metadata.create_all(engine)
