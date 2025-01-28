from fastapi import APIRouter, status, Path, HTTPException, Depends
from sqlmodel import select
from typing import Annotated

from ..database import SessionDep
from ..models import News, Employee
from ..schemas import NewsAdd, NewsPublic, NewsUpdate
from ..dependencies import get_current_user, get_user_can_add_news



router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@router.get("/", response_model=list[NewsPublic])
def get_news(current_user: Annotated[Employee, Depends(get_current_user)], session: SessionDep):
    news = session.exec(select(News)).all()
    return news

@router.get("/{id}", response_model=NewsPublic)
def get_news(id: Annotated[int, Path()], current_user: Annotated[Employee, Depends(get_current_user)], session: SessionDep):
    news = session.get(News, id)
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"news with {id} nor found")
    return news


@router.post("/", response_model=NewsPublic, status_code=status.HTTP_201_CREATED,
             description="Add new`s can only retail and office employee")

def add_news(current_user: Annotated[Employee, Depends(get_user_can_add_news)], news: NewsAdd, session: SessionDep):
    extra_data = {"owner_id": current_user.id}
    db_news = News.model_validate(news, update=extra_data)
    session.add(db_news)
    session.commit()
    session.refresh(db_news)
    return db_news


@router.put("/{id}", response_model=NewsPublic)
def update_news(current_user: Annotated[Employee, Depends(get_user_can_add_news)], id: Annotated[int, Path()], news: NewsUpdate, session: SessionDep):
    db_news = session.get(News, id)
    if not db_news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"news with {id} nor found")
    if db_news.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    news_data = news.model_dump(exclude_unset=True)
    db_news.sqlmodel_update(news_data)
    session.add(db_news)
    session.commit()
    session.refresh(db_news)
    return db_news


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_news(current_user: Annotated[Employee, Depends(get_user_can_add_news)], id: Annotated[int, Path()], session: SessionDep):
    db_news = session.get(News, id)
    if not db_news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"news with {id} nor found")
    if db_news.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    session.delete(db_news)
    session.commit()