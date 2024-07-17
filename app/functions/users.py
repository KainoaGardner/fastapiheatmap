from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


# from ..database.database import get_db
from ..database import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()


def get_all_users(db: Session):
    return db.query(models.Users).all()


def create_user(db: Session, user: schemas.UserCreate):
    password = user.password  # HASH THIS PASSWORD
    db_user = models.Users(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_user(db: Session, user_id: int):
    db_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    db.delete(db_user)
    db.commit()
