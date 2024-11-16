from typing import Optional

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .annotations import intpk, created_at, updated_at
from .base import Base


class CategoryDescription(Base):
    __tablename__ = "categories_descriptions"

    id: Mapped[intpk]

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)
    category: Mapped["Category"] = relationship(back_populates="category_description")
    title: Mapped[Optional[str]] = mapped_column(String(1024), nullable=False, unique=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, unique=False)
    meta_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, unique=False)
    meta_description: Mapped[Optional[str]] = mapped_column(String(1500), nullable=True, unique=False)
    date_added: Mapped[created_at]
    date_modified: Mapped[updated_at]
