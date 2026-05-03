from datetime import datetime
from sqlalchemy import select
from database import SessionLocale
from sqlalchemy.orm import Session
from models import Todo
from schemas import(
    ToDoCreate, 
    ToDoRead,
    ToDoUpdate,
    ReminderSet
)

def get_todos(
    db: Session,
    skip: int,
    limit: int,
    is_completed: bool | None = None) -> list[Todo]:

    statement = select(Todo).order_by(Todo.id.desc()).offset(skip).limit(limit)
    if is_completed is not None:
        statement = statement.where(Todo.is_completed == is_completed)
    
    return db.execute(statement).scalars().all()

def get_todo_by_id(db: Session, todo_id: int) -> Todo | None:
    todo = db.get(Todo, todo_id)

    return todo

def create_todo(db: Session, todo: ToDoCreate) -> Todo:
    todo_create = Todo(
        title=todo.title,
        description=todo.description,
        is_completed=todo.is_completed,
        reminder_at=todo.reminder_at)

    db.add(todo_create)
    db.commit()
    db.refresh(todo_create)

    return todo_create

def update_todo_by_id(db: Session, todo_id: int, todo_update: ToDoUpdate) -> Todo | None:
    todo = db.get(Todo, todo_id)

    if todo is None:
        return None

    if todo_update.title is not None:
        todo.title = todo_update.title

    if todo_update.description is not None:
        todo.description = todo_update.description

    if todo_update.is_completed is not None:
        todo.is_completed = todo_update.is_completed

    todo.reminder_at = todo_update.reminder_at

    db.commit()
    db.refresh(todo)

    return todo

def delete_todo_by_id(db: Session, todo_id: int) -> bool:
    todo = db.get(Todo, todo_id)

    if todo is None:
        return False
    
    db.delete(todo)
    db.commit()
    return True

def add_reminder_by_id(db: Session, todo_id: int, reminder: ReminderSet) -> Todo | None:
    todo = db.get(Todo, todo_id)

    if todo is None:
        return None
    
    todo.reminder_at = reminder.reminder_at

    db.commit()
    db.refresh(todo)
    return todo

def delete_reminder_by_id(db: Session, todo_id: int) -> Todo | None:
    todo = db.get(Todo, todo_id)

    if todo is None:
        return None
    
    todo.reminder_at = None

    db.commit()
    db.refresh(todo)
    return todo