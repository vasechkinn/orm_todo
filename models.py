from sqlalchemy.orm import(
    mapped_column,
    Mapped,
)
from datetime import datetime
from sqlalchemy import (
    String,
)
from database import Base
MAX_LENGTH = 256
MIN_LENGTH = 1

class Todo(Base):
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(MAX_LENGTH))
    description: Mapped[str] = mapped_column(String(MAX_LENGTH))
    is_completed: Mapped[bool] = mapped_column(default=False)
    reminder_at: Mapped[datetime | None] = mapped_column(default=None)