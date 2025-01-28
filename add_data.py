import requests
from app.main import app
from fastapi.testclient import TestClient
import random

client = TestClient(app)
url='http://127.0.0.1:8000/'


add_location1 = {'name': 'Retail'}
add_location12 = {'name': 'Office'}
name_location =[add_location1, add_location12]

def add_location(client: TestClient, name_location):
    for pos in name_location:
        response = client.post(f'{url}location',
                               json=pos)
    print("location done")
# add_location(client)


position_store_position = {'position': 'Area Responsble', 'location_id': 1, 'short_name': 'AR'}
position1_store_position = {'position': 'Logistic Responsble', 'location_id': 1, 'short_name': 'LR'}
position2_store_position = {'position': 'Deputy Manager', 'location_id': 1, 'short_name': 'DepSm'}
position3_store_position = {'position': 'Store Manager', 'location_id': 1, 'short_name': 'SM'}
store_position =[position_store_position, position2_store_position, position3_store_position, position1_store_position]

def add_store_position(client: TestClient):
    for pos in store_position:
        response = client.post(f'{url}store_position',
                               json=pos)
    print("store_position done")
# add_store_position(client)



position_office_department = {'position': 'Et Audit', 'location_id': 2, 'short_name': 'AU'}
position1_office_department = {'position': 'Logistic', 'location_id': 2, 'short_name': 'LOG'}
position2_office_department = {'position': 'Accounting', 'location_id': 2, 'short_name': 'ACC'}
position3_office_department = {'position': 'Facility', 'location_id': 2, 'short_name': 'FC'}
office_department =[position_office_department, position2_office_department, position3_office_department, position1_office_department]

def add_office_department(client: TestClient):
    for pos in office_department:
        response = client.post(f'{url}office_department',
                               json=pos)
    print("office_department done")
# add_office_department(client)

def add_country(client: TestClient):
    response = client.post(f'{url}country',
                           json={"name": "UA"})
    print("country done")
# add_country(client)

position_region = {'country_id': 1, 'name': 'Region1'}
position2_region = {'country_id': 1, 'name': 'Region2'}
region =[position_region, position2_region]

def add__region(client: TestClient):
    for pos in region:
        response = client.post(f'{url}region',
                               json=pos)
    print("_region done")
# add__region(client)



position_district = {'name': 'Kyiv South', 'region_id': 1, "district_manager_id":2}
position1_district = {'name': 'South', 'region_id': 1, "district_manager_id":2}
position2_district = {'name': 'Dnipro', 'region_id': 2, "district_manager_id":2}
position3_district = {'name': 'Podil', 'region_id': 1, "district_manager_id":2}
position4_district = {'name': 'Kyiv East', 'region_id': 2, "district_manager_id":2}
position5_district = {'name': 'Center', 'region_id': 1, "district_manager_id":2}
position6_district = {'name': 'West', 'region_id': 2, "district_manager_id":2}
position7_district = {'name': 'Volyn', 'region_id': 1, "district_manager_id":2}
position8_district = {'name': 'Kyiv North', 'region_id': 2, "district_manager_id":2}
district =[position_district, position2_district, position3_district, position4_district, position5_district,
            position6_district,position7_district]

def add__district(client: TestClient):
    for pos in district:
        response = client.post(f'{url}district',
                               json=pos)
    print("_district done")
# add__district(client)

stores = """"
J022
J010
J079
J087
J061
J045
J080
J007
J003
J052
J017
J082
J066
J049
J075
J057
J001
J012
J060
J047
J053
J015
J042
J056
J005
J024
J054
J014
J097
J029
J008
J032
J068
J025
J021
J074
J037
J002
J055
J039
J016
J030
J043
J072
J089
J086
J088
J027
J034
J026
J044
J035
J051
J059
J063
J046
J040
J031
J071
J077
J065
J028
J058
J092
J011
J096
J036
J019
J004
J091
J050
J023
J064
J048
J090
J083
J009
J093
J062
J070
J041
J033
J095
J038
J078
J013
J094
J081
"""

city = [i for i in "Kyiv Kharkiv Odesa Dnipro Donetsk Lviv Zaporizhzhia Kryvyi Rih Mykolaiv".split()]
def add_store(client: TestClient):
    for store in stores.split():
        response = client.post(f'{url}store',
                               json={"name": store, "city": random.choice(city),
                                     "district_id": random.choice(range(1,15))})
    print("store done")
# add_store(client)


retail_position_list = [{"short_name": "DM", "position": "District Manager", "location_id":1 }, {"short_name": "RM", "position": "Region Manager", "location_id":1 }]
def add_retail_position(client: TestClient):
    for pos in retail_position_list:
        response = client.post(f'{url}retailposition',
                               json=pos)
        print(response.json())
    print("retail_position done")

# add_retail_position(client)
#
names = """Alabama	Olivia	Charlotte	Amelia	Ava	Elizabeth
Alaska	Charlotte	Aurora	Amelia	Hazel	Emma
Arizona	Olivia	Emma	Mia	Isabella	Sophia
Arkansas	Olivia	Amelia	Charlotte	Emma	Evelyn
California	Olivia	Mia	Camila	Emma	Isabella
Colorado	Charlotte	Olivia	Sophia	Emma	Amelia
Connecticut	Olivia	Charlotte	Mia	Emma	Amelia
Delaware	Charlotte	Isabella	Emma	Olivia	Sophia
Dist. of Columbia	Charlotte	Olivia	Naomi	Sophia	Maya
Florida	Olivia	Emma	Isabella	Mia	Sophia
Georgia	Olivia	Charlotte	Amelia	Emma	Ava
Hawaii	Isla	Mia	Olivia	Luna	Ava
Idaho	Olivia	Charlotte	Evelyn	Amelia	Emma
Illinois	Olivia	Emma	Mia	Sophia	Charlotte
Indiana	Charlotte	Amelia	Olivia	Eleanor	Evelyn
Iowa	Charlotte	Olivia	Amelia	Harper	Evelyn
Kansas	Amelia	Charlotte	Olivia	Evelyn	Emma
Kentucky	Amelia	Charlotte	Emma	Olivia	Evelyn
Louisiana	Amelia	Olivia	Charlotte	Ava	Harper
Maine	Charlotte	Evelyn	Olivia	Eleanor	Harper
Maryland	Olivia	Emma	Charlotte	Sophia	Mia
Massachusetts	Charlotte	Olivia	Emma	Sophia	Isabella
Michigan	Charlotte	Amelia	Olivia	Sophia	Emma
Minnesota	Charlotte	Olivia	Evelyn	Emma	Amelia
Mississippi	Ava	Amelia	Olivia	Charlotte	Harper
Missouri	Charlotte	Olivia	Amelia	Eleanor	Harper
Montana	Charlotte	Emma	Hazel	Olivia	Amelia
Nebraska	Charlotte	Olivia	Sophia	Amelia	Evelyn
Nevada	Olivia	Isabella	Mia	Sophia	Charlotte
New Hampshire	Charlotte	Olivia	Evelyn	Amelia	Emma
New Jersey	Olivia	Emma	Mia	Sophia	Isabella
New Mexico	Olivia	Amelia	Mia	Isabella	Emma
New York	Emma	Olivia	Sophia	Mia	Amelia
North Carolina	Olivia	Amelia	Charlotte	Emma	Sophia
North Dakota	Evelyn	Charlotte	Amelia	Harper	Olivia
Ohio	Charlotte	Amelia	Olivia	Sophia	Evelyn
Oklahoma	Olivia	Amelia	Emma	Sophia	Charlotte
Oregon	Olivia	Amelia	Evelyn	Charlotte	Emma
Pennsylvania	Charlotte	Olivia	Emma	Sophia	Amelia
Rhode Island	Charlotte	Sophia	Olivia	Amelia	Emma
South Carolina	Olivia	Charlotte	Amelia	Emma	Ava
South Dakota	Ava	Charlotte	Nora	Amelia	Evelyn
Tennessee	Charlotte	Olivia	Amelia	Emma	Ava
Texas	Emma	Olivia	Camila	Mia	Isabella
Utah	Charlotte	Olivia	Emma	Evelyn	Lucy
Vermont	Amelia	Eleanor	Charlotte	Evelyn	Sophia
Virginia	Charlotte	Olivia	Emma	Sophia	Amelia
Washington	Olivia	Amelia	Emma	Sophia	Evelyn
West Virginia	Amelia	Charlotte	Harper	Olivia	Willow
Wisconsin	Charlotte	Olivia	Evelyn	Amelia	Emma
Wyoming	Evelyn	Amelia	Olivia	Harper	Charlotte"""

list_name = []
for nam in names.split():
    list_name.append(nam)


def add_employee(client: TestClient):
    for i in names.split():
        employee = {"name": i, "surname": random.choice(list_name), "email": i + '@mail.com',
                    "store_id": random.choice(range(1, 73)),
                    'store_position_name': random.choice(range(1,5))}
        response = client.post(f'{url}employee',
                               json=employee)
    print("employee_store_position done")
# add_employee(client)


def add_employee_office(client: TestClient):
    for i in names.split()[:20]:
        employee = {"name": i, "surname": random.choice(list_name), "email": i + '@mail.com',
                    'office_department_name': random.choice(range(1,5))}
        response = client.post(f'{url}employee',
                               json=employee)
    print("employee_office_department done")
# add_employee_office(client)


def add_employee_retail(client: TestClient):
    for i in names.split()[:12]:
        employee = {"name": i, "surname": random.choice(list_name), "email": i + '@mail.com',
                    'retail_position_name': random.choice(range(1,3))}
        response = client.post(f'{url}employee',
                               json=employee)
    print("retail_position_employee done")
# add_employee_retail(client)


def add_employee_retail_cm(client: TestClient):

    employee = {"name": "genya", "surname": "genya", "email": 'genya@mail.com',
                'retail_position_name': 1}
    response = client.post(f'{url}employee',
                           json=employee)
    print(response.json())
    print("CM done")
# add_employee_retail_cm(client)



def update_employee(client: TestClient):
    for i in range(1970, 1990):
        response = client.put(f'{url}employee/{i}',
                               json={'name': random.choice(list_name)})
    print("update_employee done")
# update_employee(client)

text = """Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32."""
title = [i for i in text.split()]
def add_news(client: TestClient):
    for i in range(10):
        response = client.post(f'{url}news',
                               json={"title": random.choice(title),
                                     "content": text[:random.randrange(10,40)],
                                     "owner_id": random.randrange(1, 349)})
        print(response.json())
    print("news done")
# add_news(client)

def add_competition(client: TestClient):
    for i in range(10):
        response = client.post(f'{url}competition',
                               json={"title": random.choice(title),
                                     "content": text[:random.randrange(10,40)],
                                     "owner_id": random.randrange(1, 349)})
        print(response.json())
    print("competition done")
# add_competition(client)

def add_tasks(client: TestClient):
    for i in range(10):
        response = client.post(f'{url}tasks',
                               json={"title": random.choice(title),
                                     "content": text[:random.randrange(10,40)],
                                     "owner_id": random.randrange(1, 349),
                                     "location_id": random.randrange(1,3)})
        print(response.json())
    print("tasks done")
    
# add_tasks(client)

def add_ticket(client: TestClient):
    for i in range(10):
        response = client.post(f'{url}tickets',
                               json={"title": random.choice(title),
                                     "content": text[:random.randrange(10,40)],
                                     "owner_id": random.randrange(1, 349),
                                     "location_id": random.randrange(1,3),
                                     "importantly": random.randrange(0,2)})
        print(response.json())
    print("tickets done")

# add_ticket(client)
