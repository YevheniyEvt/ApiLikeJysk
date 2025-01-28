from fastapi import FastAPI

from .routers import (tasks,
                      tickets, competition, news, auth)
from .routers.ad_to_db import (location, retail_position, store_position,
                               office_department, country, region, district, store, employee)

app = FastAPI()

app.include_router(auth.router)
app.include_router(news.router)
app.include_router(competition.router)
app.include_router(tasks.router)
app.include_router(tickets.router)



# api for add data to database

# app.include_router(location.router)
# app.include_router(retail_position.router)
# app.include_router(store_position.router)
# app.include_router(office_department.router)
# app.include_router(country.router)
# app.include_router(region.router)
# app.include_router(district.router)
# app.include_router(store.router)
app.include_router(employee.router)










@app.get('/')
def root():
    return {'message': 'Hello World1'}

