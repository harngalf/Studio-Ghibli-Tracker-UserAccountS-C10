
# SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship

# API docs connection
from src.database import Base, engine


## User DB Model
class UserM(Base):
    __tablename__ = "users"
    
    user_id = Column(
        Integer,
        primary_key=True,
        index=True
    )    
    email = Column(
        String(255),
        unique=True,
        index=True
    )
    hashed_password = Column(
        String
    )
    user_name = Column(
        String(125),
        nullable=False
    )
    profile_pic = Column(
        String(255)
    )
    is_active = Column(
        Boolean, 
        default=True
    )
   
    #user_movies_u = relationship("UserMovie", back_populates="userM")

Base.metadata.create_all(engine)