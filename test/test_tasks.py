from sqlmodel import Session
from fastapi.testclient import TestClient


def test_get_get_my_task(store_user: TestClient, session: Session):
    response = store_user.get('task/')
    assert response.status_code == 200

def test_get_task(store_user: TestClient, session: Session):
    response = store_user.get('task/1')
    assert response.json().get("id") == 1
    assert response.status_code == 200

def test_get_one_wrong_tasks(store_user: TestClient, session: Session):
    response = store_user.get('task/101')
    assert response.status_code == 404
    assert response.json().get("detail") == "task with 101 nor found"



def test_add_task_store_user(store_user: TestClient, session: Session):
    response = store_user.post('task/add', json={"title": "title",
                                     "content": "content", "task_recipient_id": 2})
    assert response.status_code == 201
    assert response.json().get("employee").get("id") == 1

def test_add_task_retail_user(retail_user: TestClient, session: Session):
    response = retail_user.post('task/add', json={"title": "title",
                                     "content": "content", "task_recipient_id": 1})
    assert response.status_code == 201
    assert response.json().get("employee").get("id") == 2

def test_add_task_office_user(office_user: TestClient, session: Session):
    response = office_user.post('task/add', json={"title": "title",
                                     "content": "content", "task_recipient_id": 1})
    assert response.status_code == 201
    assert response.json().get("employee").get("id") == 3

def test_get_my_store_task(store_user: TestClient, session: Session):
    response = store_user.get('task/department')
    assert response.status_code == 200
    print(response.json())

def test_get_my_office_task(office_user: TestClient, session: Session):
    response = office_user.get('task/department')
    assert response.status_code == 200

def test_get_my_district_task(retail_user: TestClient, session: Session):
    response = retail_user.get('task/department')
    assert response.status_code == 200

def test_data_for_task_district(retail_user: TestClient, session: Session):
    response = retail_user.get('task/add')
    assert response.status_code == 200

def test_data_for_task_office(office_user: TestClient, session: Session):
    response = office_user.get('task/add')
    assert response.status_code == 200

def test_data_for_task_store(store_user: TestClient, session: Session):
    response = store_user.get('task/add')
    assert response.status_code == 200


