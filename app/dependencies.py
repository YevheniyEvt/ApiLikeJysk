from typing import Annotated
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer

from .schemas import TokenData
from .models import Employee
from .database import SessionDep
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def verify_access_token(token: str, credentials_exception) :
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        can_add_news: bool = payload.get("can_add_news")
        can_add_competitions: bool = payload.get("can_add_competitions")
        token_data = TokenData(user_id=user_id, can_add_news=can_add_news, can_add_competitions=can_add_competitions)
    except InvalidTokenError:
        raise credentials_exception
    return token_data

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception  = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Could not validate credentials",
                                           headers={"WWW-Authenticate": "Bearer"},
                                           )

    token = verify_access_token(token, credentials_exception)
    user = session.get(Employee, token.user_id)
    return user


def get_user_can_add_news(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception  = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Could not validate credentials",
                                           headers={"WWW-Authenticate": "Bearer"},
                                           )

    token = verify_access_token(token, credentials_exception)

    can_add_news = token.can_add_news
    if not can_add_news:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not enough permissions",
                            headers={"WWW-Authenticate": "Bearer"},
                            )
    user = session.get(Employee, token.user_id)
    return user

def get_user_can_add_competitions(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception  = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Could not validate credentials",
                                           headers={"WWW-Authenticate": "Bearer"},
                                           )

    token = verify_access_token(token, credentials_exception)
    can_add_competitions = token.can_add_competitions
    if not can_add_competitions:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not enough permissions",
                            headers={"WWW-Authenticate": "Bearer"},
                            )
    user = session.get(Employee, token.user_id)
    return user