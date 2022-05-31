
# SQLAlchemy
from sqlalchemy.orm import Session

# API files
import models, schemas

# API CRUD operations
## Users
def get_user(
    db: Session, 
    user_id: int
):
    return db.query(models.UserM).filter(models.UserM.user_id == user_id).first()

def get_user_by_email(
    db: Session, 
    email: str
):
    return db.query(models.UserM).filter(models.UserM.email == email).first()

def get_user_by_id(
    db: Session, 
    user_id: int
):
    return db.query(models.UserM).filter(models.UserM.user_id == user_id).first()

def get_users(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
):
    return db.query(models.UserM).offset(skip).limit(limit).all()

def create_user(
    db: Session, 
    user: schemas.UserS
):
    fake_hashed_password = user.hashed_password + "not really hashed"
    db_user = models.UserM(
        # **user.dict()
        email=user.email,
        hashed_password=fake_hashed_password,
        user_name=user.user_name,        
        profile_pic=user.profile_pic
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(
    db: Session, 
    user: schemas.UserS
):
    fake_hashed_password = user.hashed_password + "not really hashed"
    db_user = models.UserM(
        # **user.dict()
        email=user.email,
        hashed_password=fake_hashed_password,
        user_name=user.user_name,        
        profile_pic=user.profile_pic
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

## Movies 
def get_movies(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
):
    return db.query(models.MovieM).offset(skip).limit(limit).all()


def get_movie(
    db: Session, 
    movie_id: int,
    title: str
):
    return db.query(models.MovieM).filter(models.MovieM.movie_id == movie_id).first()  

def get_movie_by_title(
    db: Session, 
    title: str
):
    return db.query(models.MovieM).filter(models.MovieM.title == title).first()

def create_movies(
    db: Session,
    movie: schemas.MovieS
):
    db_movies = models.MovieM(**movie.dict())
    db.add(db_movies)
    db.commit()
    db.refresh(db_movies)
    return db_movies


# def create_user_movies(
#     db: Session, 
#     user_movies: schemas.UserMovieCreate,
#     user_id: int,
#     movie_id: int
# ):
#     db_user_movies = models.UserMovie(
#         **user_movies.dict(),
#         userM_id=user_id,
#         movieU_id=movie_id
#     )
#     db.add(db_user_movies)
#     db.commit()
#     db.refresh(db_user_movies)    
#     return db_user_movies

# Backoffice

## Users

def get_userBO(
    db: Session, 
    user_id: int
):
    return db.query(models.UserMBO).filter(models.UserMBO.user_id == user_id).first()

def get_userBO_by_email(
    db: Session, 
    email: str
):
    return db.query(models.UserMBO).filter(models.UserMBO.email == email).first()

def get_usersBO(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
):
    return db.query(models.UserMBO).offset(skip).limit(limit).all()

def create_userBO(
    db: Session, 
    user: schemas.UserBOS
):
    fake_hashed_password = user.hashed_password + "not really hashed"
    db_user = models.UserMBO(
        # **user.dict()
        email=user.email,
        hashed_password=fake_hashed_password,
        user_name=user.user_name,        
        profile_pic=user.profile_pic
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
