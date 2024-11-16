from typing import Optional, List

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .annotations import intpk, created_at, updated_at
from .base import Base


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id: Mapped[intpk]
    products: Mapped[Optional[List["Product"]]] = relationship(back_populates="manufacturer")

    name: Mapped[str] = mapped_column(String(256), nullable=True, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    date_added: Mapped[created_at]
    date_modified: Mapped[updated_at]
