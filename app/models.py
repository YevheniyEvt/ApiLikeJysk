from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from datetime import datetime

# Локація (retail, office)
class Location(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    retail_position: list["RetailPosition"] = Relationship(back_populates='location')
    store_position: list["StorePosition"] = Relationship(back_populates="location")
    office_department: list["OfficeDepartment"] = Relationship(back_populates="location")
    tasks: list["Task"] = Relationship(back_populates="location")
    tickets: list["Ticket"] = Relationship(back_populates="location")

# посади в рітейлі DM, Rm ...
class RetailPosition(SQLModel, table=True):
    __tablename__ = 'retail_position'
    id: int = Field(default=None, primary_key=True)
    position: str
    short_name: str
    employee: list["Employee"] = Relationship(back_populates='retail_position')
    location_id: int = Field(foreign_key='location.id')
    location: Location = Relationship(back_populates="retail_position")

# посади в магазиніas. ar
class StorePosition(SQLModel, table=True):
    __tablename__ = 'store_position'
    id: int = Field(default=None, primary_key=True)
    position: str
    short_name: str
    employee: list["Employee"] = Relationship(back_populates='store_position')
    location_id: int = Field(foreign_key='location.id')
    location: Location = Relationship(back_populates="store_position")

# посади в офісі
class OfficeDepartment(SQLModel, table=True):
    __tablename__ = 'office_department'
    id: int = Field(default=None, primary_key=True)
    position: str
    short_name: str
    employee: list["Employee"] = Relationship(back_populates='office_department')
    location_id: int = Field(foreign_key='location.id')
    location: Location = Relationship(back_populates="office_department")


class Country(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    region: list["Region"] = Relationship(back_populates="country")

class Region(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    district: list["District"] = Relationship(back_populates="region")
    country_id: int = Field(foreign_key='country.id')
    country: Country = Relationship(back_populates="region")

class District(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    store: list["Store"] = Relationship(back_populates="district")
    region_id: int = Field(foreign_key='region.id')
    region: Region = Relationship(back_populates="district")
    district_manager_id: int | None = Field(foreign_key='employee.id', default=None)


class Store(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    city: str
    open: datetime = Field(default=datetime.now())
    employee: list["Employee"] = Relationship(back_populates='store')
    district_id: int = Field(foreign_key="district.id")
    district: District = Relationship(back_populates="store")


class Employee(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    surname: str
    email: EmailStr = Field(default=None)
    hired: datetime = Field(default=datetime.now())

    retail_position_name: int | None = Field(default=None, foreign_key="retail_position.id")
    retail_position: RetailPosition = Relationship(back_populates='employee')

    store_position_name: int | None = Field(default=None, foreign_key="store_position.id")
    store_position: StorePosition = Relationship(back_populates='employee')

    office_department_name: int | None = Field(default=None, foreign_key="office_department.id")
    office_department: OfficeDepartment = Relationship(back_populates='employee')

    store_id: int | None = Field(default=None, foreign_key="store.id")
    store: Store = Relationship(back_populates='employee')

    news: list["News"] = Relationship(back_populates="employee")
    competition: list["Competition"] = Relationship(back_populates="employee")
    tasks: list["Task"] = Relationship(back_populates="employee")
    tickets: list["Ticket"] = Relationship(back_populates="employee")

class User(SQLModel, table=True):
    employee_id: int = Field(foreign_key="employee.id", primary_key=True)
    password: str


class News(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default=datetime.now())
    owner_id: int = Field(foreign_key="employee.id")
    employee: Employee = Relationship(back_populates="news")


class Competition(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default=datetime.now())
    owner_id: int = Field(foreign_key="employee.id")
    employee: Employee = Relationship(back_populates="competition")

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default=datetime.now())
    task_recipient_id: int # = Field(foreign_key="employee.id")
    department: str
    owner_id: int = Field(foreign_key="employee.id")
    employee: Employee = Relationship(back_populates="tasks")
    location_id: int = Field(foreign_key="location.id")
    location: Location = Relationship(back_populates="tasks")


class Ticket(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    importantly: bool = Field(default=False)
    department: str
    created_at: datetime = Field(default=datetime.now())
    owner_id: int = Field(foreign_key="employee.id")
    employee: Employee = Relationship(back_populates="tickets")
    location_id: int = Field(foreign_key="location.id")
    location: Location = Relationship(back_populates="tickets")