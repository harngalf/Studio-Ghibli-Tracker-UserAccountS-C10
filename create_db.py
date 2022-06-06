
import database
import models 

Base = models.Base
engine = database.engine

print("creating database")

Base.metadata.create_all(bind=engine)
