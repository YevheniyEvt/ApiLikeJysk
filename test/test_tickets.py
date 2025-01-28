from sqlmodel import Session
from fastapi.testclient import TestClient

def test_add_ticket(store_user: TestClient, session: Session):
    response = store_user.post('tickets/add',
                               json={"title": "title123",
                                     "content": "content",
                                     "importantly": True,
                                     "location_name": "Retail",
                      })
    assert response.status_code == 201
    assert response.json().get("title") == "title123"
    assert response.json().get("employee").get("id") == 1

def test_add_ticket_without_tittle(store_user: TestClient, session: Session):
    response = store_user.post('tickets/add',
                               json={
                                     "content": "content",
                                     "importantly": True,
                                     "location_name": "Retail",
                      })
    assert response.status_code == 422


def test_location_name_for_ticket(store_user: TestClient, session: Session):
    response = store_user.get('tickets/add')
    assert response.status_code == 200

def test_get_my_tickets(retail_user: TestClient, session: Session):
    response = retail_user.get('tickets/')
    assert response.status_code == 200
    assert response.json()[0].get("employee").get("id") == 2

def test_get_my_department_tickets(retail_user: TestClient, session: Session):
    response = retail_user.get('tickets/department')
    assert response.status_code == 200

def test_get_my_department_tickets_store_user(store_user: TestClient, session: Session):
    response = store_user.get('tickets/department')
    assert response.status_code == 200
    assert response.json()[0].get("employee").get("id") == 1

def test_get_ticket(store_user: TestClient, session: Session):
    response = store_user.get('tickets/1')
    assert response.status_code == 200
    assert response.json().get("employee").get("id") == 1

def test_get_not_my_ticket(store_user: TestClient, session: Session):
    response = store_user.get('tickets/2')
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authorized to perform request action"

def test_get_wrong_ticket(store_user: TestClient, session: Session):
    response = store_user.get('tickets/222')
    assert response.status_code == 404
    assert response.json().get("detail") == "tickets with 222 nor found"




