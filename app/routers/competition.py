from fastapi import APIRouter, status, Path, HTTPException, Depends
from sqlmodel import select
from typing import Annotated

from ..database import SessionDep
from ..models import Competition, Employee
from ..schemas import CompetitionAdd, CompetitionPublic, CompetitionUpdate
from ..dependencies import get_current_user, get_user_can_add_competitions



router = APIRouter(
    prefix="/competition",
    tags=["Competition"]
)




@router.get("/", response_model=list[CompetitionPublic])
def get_competitions(current_user: Annotated[Employee, Depends(get_current_user)],
                     session: SessionDep):

    competition = session.exec(select(Competition)).all()
    return competition


@router.get("/{id}", response_model=CompetitionPublic)
def get_competition(current_user: Annotated[Employee, Depends(get_current_user)],
                    id: Annotated[int, Path()],  session: SessionDep):

    competition = session.get(Competition, id)
    if not competition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"competition with {id} nor found")
    return competition


@router.post("/", response_model=CompetitionPublic, status_code=status.HTTP_201_CREATED)
def add_competition(current_user: Annotated[Employee, Depends(get_user_can_add_competitions)],
                    competition: CompetitionAdd, session: SessionDep):

    extra_data = {"owner_id": current_user.id}
    db_competition = Competition.model_validate(competition, update=extra_data)
    session.add(db_competition)
    session.commit()
    session.refresh(db_competition)
    return db_competition


@router.put("/{id}", response_model=CompetitionPublic)
def update_competition(current_user: Annotated[Employee, Depends(get_user_can_add_competitions)],
                       id: Annotated[int, Path()], competition: CompetitionUpdate, session: SessionDep):
    db_competition = session.get(Competition, id)
    if not db_competition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"competition with {id} nor found")
    if db_competition.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    competition_data = competition.model_dump(exclude_unset=True)
    db_competition.sqlmodel_update(competition_data)
    session.add(db_competition)
    session.commit()
    session.refresh(db_competition)
    return db_competition


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_competition(current_user: Annotated[Employee, Depends(get_user_can_add_competitions)],
                       id: Annotated[int, Path()], session: SessionDep):
    db_competition = session.get(Competition, id)
    if not db_competition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"competition with {id} nor found")
    if db_competition.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")
    session.delete(db_competition)
    session.commit()