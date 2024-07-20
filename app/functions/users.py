from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..database import models, schemas


def get_user(db: Session, user_id: int) -> schemas.User:
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_username(db: Session, username: str) -> schemas.User:
    return db.query(models.Users).filter(models.Users.username == username).first()


def get_all_users(db: Session) -> list:
    return db.query(models.Users).all()


def get_user_all_heatmaps(user: schemas.User) -> list:
    return user.heatmaps


# def get_all_entries(heatmap_id: int, db: Session):
#     pass


def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    password = user.password  # HASH THIS PASSWORD
    db_user = models.Users(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_user(db: Session, db_user: schemas.User) -> schemas.User:
    db.delete(db_user)
    db.commit()
    return db_user
