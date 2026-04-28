from datetime import datetime
from database import Base, get_db, engine
from fastapi import (FastAPI,
                     Query,
                     Path,
                     status,
                     HTTPException,
                     Request,
                     Depends,
                     Form
                     )
from sqlalchemy.orm import Session
from fastapi.responses import (
    RedirectResponse,
    HTMLResponse,
)
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import crud, schemas

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
async def get_todos(
    db: Session = Depends(get_db),
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0)] = 100,
    is_completed: Annotated[bool | None, Query()] = None) -> list[ToDoRead]:
    todos = crud.get_todos(db, skip, limit, is_completed)
    return todos

@app.get('/todo/{todo_id}', status_code=status.HTTP_201_CREATED)
def get_todo_by_id(todo_id: Annotated[int, Path()], db: Session = Depends(get_db)) -> ToDoRead:
    result = crud.get_todo_by_id(db, todo_id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result


@app.post('/todos', status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoCreate, db: Session = Depends(get_db)) -> ToDoRead:
    todo_create = crud.create_todo(db, todo)

    return todo_create

@app.put('/todos/{todo_id}')
def update_todo_by_id(todo_id: Annotated[int, Path()],
                      todo_update: ToDoUpdate,
                      db: Session = Depends(get_db)) -> ToDoRead:
    todo = crud.update_todo_by_id(db, todo_id, todo_update)

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return todo



@app.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_by_id(
        todo_id: Annotated[int, Path()],
        db: Session = Depends(get_db)) -> None:

    res = crud.delete_todo_by_id(db, todo_id)

    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return None


@app.put('/todos/{todo_id}/reminder')
def add_reminder_by_id(
        todo_id: Annotated[int, Path()],
        reminder: ReminderSet,
        db: Session = Depends(get_db)
    ) -> ToDoRead:

    todo = crud.add_reminder_by_id(db, todo_id, reminder)

    if todo is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return todo


@app.delete('/todos/{todo_id}/reminder')
def delete_reminder_by_id(
        todo_id: Annotated[int, Path()],
        db: Session = Depends(get_db),
    ) -> ToDoRead:
    todo = crud.delete_reminder_by_id(db, todo_id)

    if todo is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return todo

# *** jinja ***
@app.get('/')
def index(request: Request,
          skip: Annotated[int, Query(ge=0)] = 0,
          limit: Annotated[int, Query(gt=0)] = 10,
          is_completed: Annotated[str | None, Query()] = None,
          db: Session = Depends(get_db)):
    status_filter = None
    if is_completed == 'true':
        status_filter = True
    elif is_completed == 'false':
        status_filter = False
    todos = crud.get_todos(db, skip, limit, status_filter)
    
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={'title': 'hello',
                 'todos': todos,
                 'skip': skip,
                 'limit': limit,
                 'is_completed': status_filter,
                 }
    )

@app.get('/todos/new')
def create_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='todo_create.html',
        context={'title': 'новая заметка'})

@app.post('/todos/create')
def create_todo_jin(
    db: Session = Depends(get_db),
    title: str = Form(..., min_length=1, max_length=256),
    description: str = Form(..., max_length=512),
    is_completed: bool = Form(default=False)):

    todo = schemas.ToDoCreate(title=title, 
                              description=description,
                               is_completed=is_completed)

    res = crud.create_todo(db, todo)

    return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)