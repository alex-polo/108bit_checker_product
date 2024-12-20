from typing import Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[int] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False, unique=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(255), unique=False)
    second_name: Mapped[Optional[str]] = mapped_column(String(255), unique=False)
    surname: Mapped[Optional[str]] = mapped_column(String(255), unique=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, unique=False, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, unique=False, default=False)
