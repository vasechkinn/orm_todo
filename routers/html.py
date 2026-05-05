from datetime import datetime, date
from database import Base, get_db, engine
from fastapi import (
    FastAPI,
    Query,
    Path,
    status,
    HTTPException,
    Request,
    Depends,
    Form,
    APIRouter
    )
from sqlalchemy.orm import Session
from typing import Annotated
import crud, schemas
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
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
def create_todo_jinj(
        request: Request,
        db: Session = Depends(get_db),
        title: str = Form(..., min_length=1, max_length=256),
        description: str = Form(..., max_length=512),
        is_completed: bool = Form(default=False),
        reminder_at: str | None = Form(None)):
    dt = None
    if reminder_at:
        try:
            dt = datetime.strptime(reminder_at, '%Y-%m-%dT%H:%M')

        except ValueError:
            return templates.TemplateResponse(
                request=request,
                name='todo_create.html',
                context={
                    'error': 'Неверный формат даты. Введите год, месяц, день',
                    'form_title': title,
                    'form_description': description,
                    'form_is_completed': is_completed,
                    'form_reminder': reminder_at
                }
            )

    try:
        todo = schemas.ToDoCreate(title=title,
                                description=description,
                                is_completed=is_completed,
                                reminder_at=dt)
    except ValidationError:
        return templates.TemplateResponse(
        request=request,
        name='todo_create.html',
        context={
            'error': f'Сегодня {datetime.now().replace(microsecond=0, second=0)}. Пожалуйста, установите напоминание на будущее',
            'form_title': title,
            'form_description': description,
            'form_is_completed': is_completed,
            'form_reminder': reminder_at
        })

    res = crud.create_todo(db, todo)

    return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)

@router.get('/todos/{todo_id}/update_form')
def update_form(
    request: Request,
    todo_id: int,
    db: Session = Depends(get_db)
    ):
    todo = crud.get_todo_by_id(db, todo_id=todo_id)

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Задача не найдена')

    return templates.TemplateResponse(
        request=request,
        name='todo_update.html',
        context={'todo': todo})

@router.post('/todos/{todo_id}/update')
def update_jin(
    request: Request,
    todo_id: int,
    db: Session = Depends(get_db),
    title: str | None = Form(None, min_length=1, max_length=256),
    description: str | None= Form(None, max_length=512),
    is_completed: bool = Form(default=False),
    reminder_at: str | None = Form(None),
    delete_reminder: bool = Form(False),
    ):

    current_todo = crud.get_todo_by_id(db, todo_id)
    if not current_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Задача не найдена')
    
    
    if delete_reminder:
        dt = None
    elif reminder_at:
        try:
            dt = datetime.strptime(reminder_at, '%Y-%m-%dT%H:%M')
        except ValueError:
            return templates.TemplateResponse(
                request=request,
                name='todo_create.html',
                context={
                    'error': 'Неверный формат даты. Введите год, месяц, день',
                    'form_title': title,
                    'form_description': description,
                    'form_is_completed': is_completed,
                    'form_reminder': reminder_at
                }
            )

    else:
        dt = current_todo.reminder_at
    
    try:
        todo = schemas.ToDoUpdate(title=title,
                            description=description,
                            is_completed=is_completed,
                            reminder_at=dt)
    except ValidationError:
        return templates.TemplateResponse(
        request=request,
        name='todo_create.html',
        context={
            'error': f'Сегодня {datetime.now().replace(microsecond=0, second=0)}. Пожалуйста, установите напоминание на будущее',
            'form_title': title,
            'form_description': description,
            'form_is_completed': is_completed,
            'form_reminder': reminder_at
        })

    res = crud.update_todo_by_id(db, todo_id, todo)

    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Задача не найдена')


    return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)

@router.get('/todos/{todo_id}/delete_form')
def delete_form(
    request: Request,
    todo_id: int,
    db: Session = Depends(get_db)):
    todo = crud.get_todo_by_id(db, todo_id)

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Задача не найдена')

    return templates.TemplateResponse(
        request=request,
        name='todo_delete.html',
        context={'todo': todo})

@router.post('/todos/{todo_id}/delete')
def delete_jinj(todo_id: int, db: Session = Depends(get_db)):
    crud.delete_todo_by_id(db, todo_id)
    return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)
