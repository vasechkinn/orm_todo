from datetime import datetime
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator
)

MAX_LENGTH = 256
MIN_LENGTH = 1

class ToDoCreate(BaseModel):
    title: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    description: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    is_completed: bool = False
    reminder_at: datetime | None = None

    @field_validator('reminder_at')
    @classmethod
    def validate_reminder(cls, reminder: datetime | None) -> datetime | None:
        if reminder is not None and reminder < datetime.now():
            raise ValueError('напоминание можно поставить только на будущее')
        return reminder

class ToDoUpdate(BaseModel):
    title: str | None = Field(None, min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    description: str | None = Field(None, min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    is_completed: bool | None = None
    reminder_at: datetime | None = None

    @field_validator('reminder_at')
    @classmethod
    def validate_reminder(cls, reminder: datetime | None) -> datetime | None:
        if reminder is not None and reminder < datetime.now():
            raise ValueError('напоминание можно поставить только на будущее')
        return reminder

class ReminderSet(BaseModel):
    reminder_at: datetime

class ToDoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    description: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    is_completed: bool = False
    reminder_at: datetime | None