from sqlmodel import Session
from fastapi.testclient import TestClient


def test_get_competition(client: TestClient, session: Session, store_user):
    response = client.get('competition/')
    assert response.status_code == 200

def test_get_one_competition(client: TestClient, session: Session, store_user):
    response = client.get('competition/1')
    assert response.json().get("id") == 1
    assert response.status_code == 200

def test_get_one_wrong_competition(client: TestClient, session: Session, store_user):
    response = client.get('competition/10')
    assert response.status_code == 404
    assert response.json().get("detail") == "competition with 10 nor found"


def test_store_user_add_competition(client: TestClient, session: Session, store_user):
    response = client.post('competition/', json={"title": "title",
                                     "content": "content"})
    assert response.status_code == 401
    assert response.json().get("detail") == "Not enough permissions"

def test_store_user_update_competition(client: TestClient, session: Session, store_user):
    response = client.put('competition/1', json={"title": "title123",
                                     "content": "content"})
    assert response.status_code == 401
    assert response.json().get("detail") == "Not enough permissions"

def test_store_user_delete_competition(client: TestClient, session: Session, store_user):
    response = client.delete('competition/1')
    assert response.status_code == 401
    assert response.json().get("detail") == "Not enough permissions"

def test_retail_user_add_competition(client: TestClient, session: Session, retail_user):
    response = client.post('competition/', json={"title": "title123",
                                     "content": "content"})
    assert response.status_code == 201
    assert response.json().get("title") == "title123"

def test_retail_user_update_competition(client: TestClient, session: Session, retail_user):
    response = client.put('competition/2', json={"title": "title123",
                                     "content": "content"})
    assert response.status_code == 200
    assert response.json().get("title") == "title123"

def test_retail_user_delete_competition(client: TestClient, session: Session, retail_user):
    response = client.delete('competition/2')
    assert response.status_code == 204

def test_office_user_add_competition(client: TestClient, session: Session, office_user):
    response = client.post('competition/', json={"title": "title",
                                     "content": "content"})
    assert response.status_code == 401
    assert response.json().get("detail") == "Not enough permissions"

def test_office_user_update_competition(client: TestClient, session: Session, office_user):
    response = client.put('competition/3', json={"title": "title123",
                                     "content": "content"})
    assert response.status_code == 401
    assert response.json().get("detail") == "Not enough permissions"

def test_office_user_delete_competition(client: TestClient, session: Session, office_user):
    response = client.delete('competition/3')
    assert response.status_code == 401


def test_retail_user_update_wrong_id_competition(client: TestClient, session: Session, retail_user):
    response = client.put('competition/111', json={"title": "title123",
                                            "content": "content"})
    assert response.status_code == 404
    assert response.json().get("detail") == "competition with 111 nor found"

def test_retail_user_update_wrong_owner_competition(client: TestClient, session: Session, retail_user):
    response = client.put('competition/3', json={"title": "title123",
                                          "content": "content"})
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authorized to perform request action"







