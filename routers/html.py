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
from fastapi.templating import Jinja2Templates

from fastapi.responses import (
    RedirectResponse,
    HTMLResponse,
)

templates = Jinja2Templates(directory='templates')

router = APIRouter()

@router.get('/')
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

@router.get('/todos/new')
def create_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='todo_create.html',
        context={'title': 'новая заметка'})


@router.post('/todos/create')
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

@router.get('todos/update_form')
def create_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='update.html',
        context={'title': 'отредактированная заметка'})

@router.post('/todos/update')
def create_update_jin(
        db: Session = Depends(get_db),
        title: str | None = Form(None, min_length=1, max_length=256),
        description: str | None= Form(None, max_length=512),
        is_completed: bool = Form(default=False)
        ):
    todo = schemas.ToDoUpdate(title=title,
                              description=description,
                              is_completed=is_completed)

    # res = crud.update_todo_by_id(db, todo_id=id, todo)

    return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)