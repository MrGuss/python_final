"""
В этом файле описываются ORM-модели Auth Service. Минимально должна быть модель User. В ней должны быть поля id, email (уникальный), password_hash, role, created_at. Важно: в таблице должен быть уникальный индекс по email, чтобы база сама защищала от дублей. В этом файле не должно быть бизнес-логики регистрации или логина.
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
