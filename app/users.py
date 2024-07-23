from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session

from .database import schemas
from .functions import users
from .functions.authentication import user_dependency
from .database.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/all/", response_model=list[schemas.User])  # PROBABLLY REMOVE THIS ONE
def get_all_users(db: Session = Depends(get_db)):
    db_user = users.get_all_users(db)
    return db_user


@router.get("/", response_model=schemas.User)
def get_user(user_auth: user_dependency, db: Session = Depends(get_db)):
    user_id = user_auth["id"]
    db_user = users.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = users.get_user_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return users.create_user(db, user)


@router.delete("/remove/", response_model=schemas.User)
def remove_user(user_auth: user_dependency, db: Session = Depends(get_db)):
    user_id = user_auth["id"]
    db_user = users.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return users.remove_user(db, db_user)
