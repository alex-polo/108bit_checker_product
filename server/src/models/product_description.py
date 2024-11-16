from typing import Optional

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .annotations import intpk, created_at, updated_at
from .base import Base


class ProductDescription(Base):
    __tablename__ = "products_descriptions"

    id: Mapped[intpk]
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    product: Mapped["Product"] = relationship(back_populates="product_description")

    title: Mapped[str] = mapped_column(String(1024), nullable=True, unique=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, unique=False)
    meta_title: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True, unique=False)
    meta_description: Mapped[Optional[str]] = mapped_column(String(4096), nullable=True, unique=False)
    date_added: Mapped[created_at]
    date_modified: Mapped[updated_at]