
from database import Base, engine
from models import movies_mod, user_mod, user_movies_mod

print("creating database")

Base.metadata.create_all(engine)
