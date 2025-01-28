import pytest
import random
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient

from sqlmodel import Session, SQLModel, create_engine
from app.main import app
from app.database import get_session
from app import models
from app.utils import get_password_hash, access_token_data
from app.dependencies import create_access_token
import add_data

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        'sqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name='client')
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(name='add_data')
def add_data_for_test(session: Session):
    for pos in add_data.name_location:
        location = models.Location(**pos)
        session.add(location)
        session.commit()
    #print("location done")

    for pos in add_data.store_position:
        store_position = models.StorePosition(**pos)
        session.add(store_position)
        session.commit()
    #print("store_position done")

    for pos in add_data.office_department:
        office_department = models.OfficeDepartment(**pos)
        session.add(office_department)
        session.commit()
    #print("office_department done")

    for pos in add_data.retail_position_list:
        retail_position = models.RetailPosition(**pos)
        session.add(retail_position)
        session.commit()
    #print("retail_position done")

    country = models.Country(name='UA')
    session.add(country)
    session.commit()
    #print("country done")

    for pos in add_data.region:
        region = models.Region(**pos)
        session.add(region)
        session.commit()
    #print("_region done")

    for pos in add_data.district:
        district = models.District(**pos)
        session.add(district)
        session.commit()
    #print("district done")

    for store in add_data.stores.split()[:3]:
        data_store={"name": store, "city": random.choice(add_data.city), "district_id": random.choice(range(1,3))}
        stores = models.Store(**data_store)
        session.add(stores)
        session.commit()
    #print("store done")

    data_employee = {"name": "genya1", "surname": "genya", "email": 'genya@mail.com',
                "store_position_name": 1, "store_id": 1}
    employee = models.Employee(**data_employee)
    session.add(employee)
    session.commit()
    #print("CM done")
    data_employee2 = {"name": "genya2", "surname": "genya", "email": 'genya@mail.com',
                'retail_position_name': 1}
    employee = models.Employee(**data_employee2)
    session.add(employee)
    session.commit()
    #print("CM done")
    data_employee3 = {"name": "genya3", "surname": "genya", "email": 'genya@mail.com',
                "office_department_name": 1}
    employee = models.Employee(**data_employee3)
    session.add(employee)
    session.commit()
    #print("CM done")

    # for i in add_data.names.split()[:5]:
    #     data_employee = {"name": i, "surname": random.choice(add_data.list_name), "email": i + '@mail.com',
    #                 "store_id": random.choice(range(1, 5)),
    #                 'store_position_name': random.choice(range(1,5))}
    #     employee = models.Employee(**data_employee)
    #
    #     session.add(employee)
    #     session.commit()
    # #print("employee_store_position done")
    #
    # for i in add_data.names.split()[:2]:
    #     data_employee = {"name": i, "surname": random.choice(add_data.list_name), "email": i + '@mail.com',
    #                 'office_department_name': random.choice(range(1,5))}
    #     employee = models.Employee(**data_employee)
    #     session.add(employee)
    #     session.commit()
    # #print("employee_office_department done")
    #
    # for i in add_data.names.split()[:2]:
    #     data_employee = {"name": i, "surname": random.choice(add_data.list_name), "email": i + '@mail.com',
    #                 'retail_position_name': random.choice(range(1,3))}
    #     employee = models.Employee(**data_employee)
    #     session.add(employee)
    #     session.commit()
    #print("retail_position_employee done")



    for i in range(1,4):
        data_news={"title": random.choice(add_data.title),
                                     "content": add_data.text[:random.randrange(10,40)],
                                     "owner_id": i}
        news = models.News(**data_news)
        session.add(news)
        session.commit()
    #print("news done")

    for i in range(1,4):
        data_competition={"title": random.choice(add_data.title),
                                     "content": add_data.text[:random.randrange(10,40)],
                                     "owner_id": i}
        competition = models.Competition(**data_competition)
        session.add(competition)
        session.commit()
    #print("competition done")


    for i in range(1,4):
        data_tasks={"title": random.choice(add_data.title),
                                     "content": add_data.text[:random.randrange(10, 40)],
                                     "owner_id": i,
                                     "location_id": random.randrange(1, 3),
                                    "task_recipient_id":random.randrange(1, 4),
                    "department": "J022"
                        }
        tasks = models.Task(**data_tasks)
        session.add(tasks)
        session.commit()
    ##print("tasks done")

    for i in range(1,4):
        data_tickets={"title": random.choice(add_data.title),
                                     "content": add_data.text[:random.randrange(10,40)],
                                     "owner_id": i,
                                     "location_id": random.randrange(1,3),
                                     "importantly": random.randrange(0,2),
                                     "department": "Kyiv South",
                      }
        tickets = models.Ticket(**data_tickets)
        session.add(tickets)
        session.commit()
        session.refresh(tickets)

    #print("tickets done")

@pytest.fixture(name="user")
def create_user(add_data, session: Session):
    for i in range(1,4):
        new_user = models.User.model_validate({"employee_id": i, "password": get_password_hash("password")})
        session.add(new_user)
        session.commit()

@pytest.fixture(name='store_user')
def create_auth_store_user(client: TestClient, user, session: Session):
    store_user = session.get(models.User, 1)
    token_data = access_token_data(session, store_user)
    access_token = create_access_token(data=token_data)
    client.headers = {**client.headers,
                      'Authorization': f'Bearer {access_token}'}

    return client

@pytest.fixture(name='retail_user')
def create_auth_retail_user(client: TestClient, user, session: Session):
    retail_user = session.get(models.User, 2)
    token_data = access_token_data(session, retail_user)
    access_token = create_access_token(data=token_data)
    client.headers = {**client.headers,
                      'Authorization': f'Bearer {access_token}'}
    return client

@pytest.fixture(name='office_user')
def create_auth_office_user(client: TestClient, user, session: Session):
    office_user = session.get(models.User, 3)
    token_data = access_token_data(session, office_user)
    access_token = create_access_token(data=token_data)
    client.headers = {**client.headers,
                      'Authorization': f'Bearer {access_token}'}
    return client


