import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# from jwt.exceptions import InvaliedTokenError

from .database.database import get_db
from .database import schemas
from .functions import users

from dotenv.main import load_dotenv
import os


load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_time: timedelta | None = None):
    encode = data.copy()
    if expires_time:
        expire = datetime.now(timezone.utc) + expires_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    encode.update({"exp": expire})
    encoded_jwt = jwt.encode(encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        recived_data = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = recived_data.get("username")
        if not username:
            raise credentials_exception

        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    Session = Depends(get_db)
    user = users.get_user_username(Session, username)
    if not user:
        raise credentials_exception
    return user
