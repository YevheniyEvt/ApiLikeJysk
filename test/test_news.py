from sqlmodel import Session
from fastapi.testclient import TestClient


def test_get_news(client: TestClient, session: Session, store_user):
    response = client.get('news/')
    assert response.status_code == 200

def test_get_one_news(client: TestClient, session: Session, store_user):
    response = client.get('news/1')
    assert response.json().get("id") == 1
    assert response.status_code == 200

def test_get_one_wrong_news(client: TestClient, session: Session, store_user):
    response = client.get('news/10')
    assert response.status_code == 404
    assert response.json().get("detail") == "news with 10 nor found"


def test_store_user_add_news(client: TestClient, session: Session, store_user):
    response = client.post('news/')
    assert response.status_code == 401
    assert response.json().get("detail") == "Not enough permissions"

def test_store_user_update_news(client: TestClient, session: Session, store_user):
    response = client.put('news/1')
    assert response.status_code == 401
    assert response.json().get("detail") == "Not enough permissions"

def test_store_user_delete_news(client: TestClient, session: Session, store_user):
    response = client.delete('news/1')
    assert response.status_code == 401
    assert response.json().get("detail") == "Not enough permissions"

def test_retail_user_add_news(client: TestClient, session: Session, retail_user):
    response = client.post('news/', json={"title": "title123",
                                     "content": "content"})
    assert response.status_code == 201
    assert response.json().get("title") == "title123"

def test_retail_user_update_news(client: TestClient, session: Session, retail_user):
    response = client.put('news/2', json={"title": "title123",
                                     "content": "content"})
    assert response.status_code == 200
    assert response.json().get("title") == "title123"

def test_retail_user_delete_news(client: TestClient, session: Session, retail_user):
    response = client.delete('news/2')
    assert response.status_code == 204

def test_office_user_add_news(client: TestClient, session: Session, office_user):
    response = client.post('news/', json={"title": "title123",
                                     "content": "content"})
    assert response.status_code == 201
    assert response.json().get("title") == "title123"

def test_office_user_update_news(client: TestClient, session: Session, office_user):
    response = client.put('news/3', json={"title": "title123",
                                     "content": "content"})
    assert response.status_code == 200
    assert response.json().get("title") == "title123"

def test_office_user_delete_news(client: TestClient, session: Session, office_user):
    response = client.delete('news/3')
    assert response.status_code == 204


def test_retail_user_update_wrong_id_news(client: TestClient, session: Session, retail_user):
    response = client.put('news/111', json={"title": "title123",
                                            "content": "content"})
    assert response.status_code == 404
    assert response.json().get("detail") == "news with 111 nor found"

def test_retail_user_update_wrong_owner_news(client: TestClient, session: Session, retail_user):
    response = client.put('news/3', json={"title": "title123",
                                          "content": "content"})
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authorized to perform request action"

def test_office_user_delete_wrong_id_news(client: TestClient, session: Session, office_user):
    response = client.put('news/111', json={"title": "title123",
                                            "content": "content"})
    assert response.status_code == 404
    assert response.json().get("detail") == "news with 111 nor found"

def test_office_user_delete_wrong_owner_news(client: TestClient, session: Session, office_user):
    response = client.put('news/2', json={"title": "title123",
                                          "content": "content"})
    assert response.status_code == 403
    assert response.json().get("detail") == "Not authorized to perform request action"





