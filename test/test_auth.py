from sqlmodel import Session
from fastapi.testclient import TestClient


def test_login_correct_user(client: TestClient, session: Session, user):
    response = client.post('login/',
                           data={"username": "100002", "password": "password"})
    assert response.json().get("token_type") == "bearer"
    assert len(response.json().get("access_token")) == 177

def test_login_wrong_user_id(client: TestClient, session: Session, user):
    response = client.post('login/',
                           data={"username": "100010", "password": "password"})
    assert response.status_code == 404
    assert response.json().get("detail") == "Incorrect username or password"

def test_login_wrong_user_password(client: TestClient, session: Session, user):
    response = client.post('login/',
                           data={"username": "10002", "password": "password1234"})
    assert response.status_code == 404
    assert response.json().get("detail") == "Incorrect username or password"


def test_login_wrong_id(client: TestClient, session: Session):
    response = client.post('login/',
                           data={"username": "123", "password": "0000"})
    assert response.status_code == 404
    assert response.json().get("detail") == "Incorrect username or password"

def test_login_password_0000(client: TestClient, session: Session, add_data):
    response = client.post('login/',
                           data={"username": "100002", "password": "0000"})
    assert response.status_code == 401
    assert response.json().get("detail") =='User 100002 must change password'


def test_change_password(client: TestClient, add_data):
    response = client.post('login/changepassword/',
                           data={"username": "100001", "password": "password"})
    assert response.json().get("message") == "OK"
    assert response.status_code == 201

def test_change_password_0000(client: TestClient, add_data):
    response = client.post('login/changepassword/',
                           data={"username": "100001", "password": "0000"})
    assert response.status_code == 403
    assert response.json().get("detail") == "Incorrect username or password"

def test_change_password_wrong_id(client: TestClient, add_data):
    response = client.post('login/changepassword/',
                           data={"username": "123", "password": "password"})
    assert response.status_code == 404
    assert response.json().get("detail") == "Incorrect username or password"




