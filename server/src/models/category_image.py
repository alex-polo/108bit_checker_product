from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .annotations import intpk, created_at, updated_at
from .base import Base


class CategoryImage(Base):
    __tablename__ = "category_images"

    id: Mapped[intpk]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="category_image")
    image: Mapped["Storage"] = relationship(back_populates="category_image")
    name: Mapped[Optional[str]] = mapped_column(String(1024), nullable=False, unique=True)
    date_added: Mapped[created_at]
    date_modified: Mapped[updated_at]
