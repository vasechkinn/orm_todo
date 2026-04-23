from datetime import datetime
from database import Base, get_db, engine
from fastapi import (FastAPI,
                     Query,
                     Path,
                     status,
                     HTTPException,
                     Request,)

from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import crud

from schemas import(
    ToDoCreate, 
    ToDoRead,
    ToDoUpdate,
    ReminderSet
)
app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.on_event('startup')
def startup():
    Base.metadata.create_all(engine)


@app.get('/todo')
async def get_todos(skip: Annotated[int, Query(ge=0)] = 0,
                    limit: Annotated[int, Query(gt=0)] = 100,
                    is_completed: Annotated[bool | None, Query()] = None) -> list[ToDoRead]:
    db = next(get_db())
    todos = crud.get_todos(db, skip, limit, is_completed)
    return todos

@app.get('/todo/{todo_id}', status_code=status.HTTP_201_CREATED)
def get_todo_by_id(todo_id: Annotated[int, Path()]) -> ToDoRead:
    db = next(get_db())
    result = crud.get_todo_by_id(db, todo_id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result


@app.post('/todos', status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoCreate) -> ToDoRead:
    db = next(get_db())
    todo_create = crud.create_todo(db, todo)

    return todo_create

@app.put('/todos/{todo_id}')
def update_todo_by_id(todo_id: Annotated[int, Path()],
                      todo_update: ToDoUpdate) -> ToDoRead:
    db = next(get_db())
    todo = crud.update_todo_by_id(db, todo_id, todo_update)

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return todo



@app.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_by_id(
        todo_id: Annotated[int, Path()]) -> None:
    db = next(get_db())

    res = crud.delete_todo_by_id(db, todo_id)

    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return None


@app.put('/todos/{todo_id}/reminder')
def add_reminder_by_id(
        todo_id: Annotated[int, Path()],
        reminder: ReminderSet
    ) -> ToDoRead:
    db = next(get_db())

    todo = crud.add_reminder_by_id(db, todo_id, reminder)

    if todo is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return todo


@app.delete('/todos/{todo_id}/reminder')
def delete_reminder_by_id(
        todo_id: Annotated[int, Path()]
    ) -> ToDoRead:
    db = next(get_db())

    todo = crud.delete_reminder_by_id(db, todo_id)

    if todo is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return todo

# *** jinja ***
@app.get('/')
def index(request: Request,
          skip: Annotated[int, Query(ge=0)] = 0,
          limit: Annotated[int, Query(gt=0)] = 100,
          is_completed: Annotated[bool | None, Query()] = None):
    db = next(get_db())
    todos = crud.get_todos(db, skip, limit, is_completed)
    
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={'title': 'hello',
                 'todos': todos}
    )