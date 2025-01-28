from fastapi import APIRouter, status, Path, HTTPException
from sqlmodel import select
from typing import Annotated

from app.database import SessionDep
from app.models import Country
from app.schemas import CountryAdd, CountryPublic, CountryUpdate



router = APIRouter(
    prefix="/country",
    tags=["Country"]
)


@router.post("/", response_model=CountryPublic, status_code=status.HTTP_201_CREATED)
def add_country(country: CountryAdd, session: SessionDep):
    db_country = Country.model_validate(country)
    session.add(db_country)
    session.commit()
    session.refresh(db_country)
    return db_country


@router.get("/", response_model=list[CountryPublic])
def get_country(session: SessionDep):
    country = session.exec(select(Country)).all()
    return country


@router.put("/{id}", response_model=CountryPublic)
def update_country(id: Annotated[int, Path()], country: CountryUpdate, session: SessionDep):
    db_country = session.get(Country, id)
    if not db_country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"country with {id} nor found")

    country_data = country.model_dump(exclude_unset=True)
    db_country.sqlmodel_update(country_data)
    session.add(db_country)
    session.commit()
    session.refresh(db_country)
    return db_country


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_country(id: Annotated[int, Path()], session: SessionDep):
    db_country = session.get(Country, id)
    if not db_country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"country with {id} nor found")
    session.delete(db_country)
    session.commit()