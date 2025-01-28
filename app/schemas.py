from sqlmodel import SQLModel
from datetime import datetime
from pydantic import EmailStr


# Локація (retail, office)
class LocationBase(SQLModel):
    name: str

class LocationAdd(LocationBase):
    pass

class LocationPublic(LocationBase):
    id: int

class LocationPublicWithRetail(LocationPublic):
    retail_position: list["RetailPositionPublic"]

class LocationPublicWithStore(LocationPublic):
    store_position: list["StorePositionPublic"]

class LocationPublicWithOffice(LocationPublic):
    office_department: list["OfficeDepartmentPublic"]

class LocationUpdate(LocationBase):
    pass



class PositionBase(SQLModel):
    position: str
    short_name: str


# посади в рітейлі DM, Rm ...
class RetailPositionAdd(PositionBase):
    location_id: int

class RetailPositionPublic(PositionBase):
    location: LocationPublic

class RetailPositionPublicWithEmployee(RetailPositionPublic):
    employee: list["EmployeePublic"]

class RetailPositionUpdate(PositionBase):
    location_id: int

# посади в магазиніas. ar
class StorePositionAdd(PositionBase):
    location_id: int
class StorePositionPublic(PositionBase):

    location: LocationPublic


class StorePositionPublicWithEmployee(PositionBase):
    employee: list["EmployeePublicForDistrict"]

class StorePositionUpdate(PositionBase):
    location_id: int

# посади в офісі
class OfficeDepartmentAdd(PositionBase):
    location_id: int

class OfficeDepartmentPublic(PositionBase):
    location: LocationPublic

class OfficeDepartmentPublicWithEmployee(OfficeDepartmentPublic):
    employee: list["EmployeePublic"]

class OfficeDepartmentUpdate(PositionBase):
    location_id: int

class LocationsForTicket(SQLModel):
    names: list

class CountryRegionDistrictBase(SQLModel):
    name: str

class CountryAdd(CountryRegionDistrictBase):
    pass

class CountryPublic(CountryRegionDistrictBase):
    id: int

class CountryPublicWithRegion(CountryRegionDistrictBase):
    region: list["RegionPublic"]

class CountryUpdate(CountryRegionDistrictBase):
    pass


class RegionAdd(CountryRegionDistrictBase):
    country_id: int

class RegionPublic(CountryRegionDistrictBase):
    country: CountryPublic
    id: int

class RegionPublicWithDistricts(RegionPublic):
    district: list["DistrictPublic"]

class RegionUpdate(RegionAdd):
    pass


class DistrictAdd(CountryRegionDistrictBase):
    region_id: int

class DistrictPublic(CountryRegionDistrictBase):
    id: int
    region: CountryRegionDistrictBase


class DistrictPublicWithStores(DistrictPublic):
    store: list["StorePublicWithEmployeeForDistrict"]

class DistrictUpdate(DistrictAdd):
    pass



class StoreBase(SQLModel):
    name: str
    city: str

class StoreAdd(StoreBase):
    district_id: int

class StorePublic(StoreBase):
    id: int
    district: DistrictPublic

class StorePublicWithEmployee(StorePublic):
    employee: list["EmployeePublic"]

class StorePublicWithEmployeeForDistrict(StorePublic):
    employee: list["EmployeePublicForDistrict"]


class StoreUpdate(StoreAdd):
    pass



class EmployeeBase(SQLModel):
    name: str
    surname: str

class EmployeeAdd(EmployeeBase):
    store_id: int | None = None
    email: EmailStr
    retail_position_name: int | None = None
    store_position_name: int | None = None
    office_department_name: int | None = None

class EmployeePublic(EmployeeBase):
    id: int
    store_position: StorePositionPublic | None = None
    store: StorePublic | None = None
    office_department: OfficeDepartmentPublic | None = None
    retail_position: RetailPositionPublic | None = None


class EmployeePublicRetail(EmployeeBase):
    retail_position_name: RetailPositionPublic

class EmployeePublicOffice(EmployeeBase):
    office_department_name: OfficeDepartmentPublic

class EmployeePublicStore(EmployeeBase):
    store_position_name: StorePositionPublic
    store: StorePublic

class EmployeePublicWithNews(EmployeePublic):
    news: list["NewsPublic"]

class EmployeePublicWithTasks(EmployeePublic):
    tasks: list["TaskPublic"]

class EmployeePublicWithCompetitions(EmployeePublic):
    competition: list["CompetitionPublic"]

class EmployeePublicForDistrict(EmployeeBase):
    id: int


class EmployeeUpdate(EmployeeBase):
    name: str | None = None
    surname: str | None = None
    store_id: int | None = None
    email: EmailStr | None = None
    retail_position_name: int | None = None
    store_position_name: int | None = None
    office_department_name: int | None = None



class NewsCompetitionBase(SQLModel):
    title: str
    content: str

class NewsAdd(NewsCompetitionBase):
    pass

class NewsPublic(NewsCompetitionBase):
    id: int
    created_at: datetime
    owner_id: int
    employee: EmployeeBase



class NewsUpdate(NewsAdd):
    pass


class CompetitionAdd(NewsCompetitionBase):
    pass

class CompetitionPublic(NewsCompetitionBase):
    id: int
    created_at: datetime
    owner_id: int
    employee: EmployeeBase

class CompetitionUpdate(NewsAdd):
    pass


class TaskTicketBase(SQLModel):
    title: str
    content: str

class TaskAdd(TaskTicketBase):
    task_recipient_id: int


class TaskPublic(TaskTicketBase):
    id: int
    department: str
    task_recipient_id: int
    created_at: datetime
    employee: EmployeePublic
    location: LocationPublic

class TaskUpdate(TaskAdd):
    pass


class TicketAdd(TaskTicketBase):
    location_name: str
    importantly: bool

class TicketPublic(TaskTicketBase):
    id: int
    department: str
    created_at: datetime
    employee: EmployeePublic


class TicketUpdate(TicketAdd):
    pass



class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    user_id: int | None = None
    can_add_news: bool | None = None
    can_add_competitions: bool | None = None