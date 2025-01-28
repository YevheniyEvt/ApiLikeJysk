from passlib.context import CryptContext
from fastapi.security import OAuth2AuthorizationCodeBearer

from .database import SessionDep
from .models import Employee, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
USER_LOGIN = 100000

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(session: SessionDep, username: str, password: str):
    user = session.get(User, int(username) - USER_LOGIN)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def can_add_news(session: SessionDep, user: User):
    employee = session.get(Employee, user.employee_id)
    if employee.office_department_name is not None or  employee.retail_position_name is not None:
        return True
    return False

def can_add_competitions(session: SessionDep, user: User):
    employee = session.get(Employee, user.employee_id)
    return employee.retail_position_name is not None

def access_token_data(session: SessionDep, user: User):
    user_can_add_news = can_add_news(session, user)
    user_can_add_competitions = can_add_competitions(session, user)
    if user_can_add_news and user_can_add_competitions:
        data = {"user_id": user.employee_id, "can_add_news": 1, "can_add_competitions": 1}
    elif user_can_add_news and not user_can_add_competitions:
        data = {"user_id": user.employee_id, "can_add_competitions": 0, "can_add_news": 1}
    else:
        data = {"user_id": user.employee_id, "can_add_competitions": 0, "can_add_news": 0}
    return data