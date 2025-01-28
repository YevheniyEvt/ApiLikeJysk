from fastapi import APIRouter, status, Path, HTTPException, Depends
from sqlmodel import select
from typing import Annotated
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..database import SessionDep
from ..models import Employee, User
from  ..utils import authenticate_user, get_password_hash, access_token_data
from ..dependencies import create_access_token
from ..schemas import Token

USER_LOGIN = 100000

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)


@router.post("/", response_model=Token)
def user_login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()] , session: SessionDep):
    employee = session.get(Employee, int(user_credentials.username)-USER_LOGIN)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect username or password")

    user = authenticate_user(session, user_credentials.username, user_credentials.password)
    if not user and user_credentials.password == "0000":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"User {user_credentials.username} must change password")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"},)

    token_data = access_token_data(session, user)
    access_token = create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/changepassword", status_code=status.HTTP_201_CREATED)
def change_password(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()] , session: SessionDep):
    user_id = int(user_credentials.username)-USER_LOGIN

    if user_credentials.password == "0000":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Incorrect username or password")


    db_employee = session.get(Employee, user_id)
    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect username or password")

    new_user = User.model_validate({"employee_id": user_id, "password": get_password_hash(user_credentials.password)})
    session.add(new_user)
    session.commit()

    return {"message": "OK"}

