from datetime import datetime
from database import Base, get_db, engine
from fastapi import (FastAPI,
                     Query,
                     Path,
                     status,
                     HTTPException,
                     Request,
                     Depends,
                     Form,
                    APIRouter,
                     )
from sqlalchemy.orm import Session
from typing import Annotated
import crud, schemas

from schemas import(
    ToDoCreate,
    ToDoRead,
    ToDoUpdate,
    ReminderSet
)

router = APIRouter(prefix='/api')


@router.get('/todo')
async def get_todos(
        db: Session = Depends(get_db),
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(gt=0)] = 100,
        is_completed: Annotated[bool | None, Query()] = None) -> list[ToDoRead]:
    todos = crud.get_todos(db, skip, limit, is_completed)
    return todos


@router.get('/todo/{todo_id}', status_code=status.HTTP_201_CREATED)
def get_todo_by_id(todo_id: Annotated[int, Path()], db: Session = Depends(get_db)) -> ToDoRead:
    result = crud.get_todo_by_id(db, todo_id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result


@router.post('/todos', status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoCreate, db: Session = Depends(get_db)) -> ToDoRead:
    todo_create = crud.create_todo(db, todo)

    return todo_create


@router.put('/todos/{todo_id}')
def update_todo_by_id(todo_id: Annotated[int, Path()],
                      todo_update: ToDoUpdate,
                      db: Session = Depends(get_db)) -> ToDoRead:
    todo = crud.update_todo_by_id(db, todo_id, todo_update)

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return todo


@router.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_by_id(
        todo_id: Annotated[int, Path()],
        db: Session = Depends(get_db)) -> None:
    res = crud.delete_todo_by_id(db, todo_id)

    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return None


@router.put('/todos/{todo_id}/reminder')
def add_reminder_by_id(
        todo_id: Annotated[int, Path()],
        reminder: ReminderSet,
        db: Session = Depends(get_db)
) -> ToDoRead:
    todo = crud.add_reminder_by_id(db, todo_id, reminder)

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return todo


@router.delete('/todos/{todo_id}/reminder')
def delete_reminder_by_id(
        todo_id: Annotated[int, Path()],
        db: Session = Depends(get_db),
) -> ToDoRead:
    todo = crud.delete_reminder_by_id(db, todo_id)

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return todo