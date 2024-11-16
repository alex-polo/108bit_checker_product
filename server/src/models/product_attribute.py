from typing import Optional

from sqlalchemy import Integer, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from .annotations import intpk, created_at, updated_at
from .base import Base


class ProductAttribute(Base):
    __tablename__ = "product_attributes"

    id: Mapped[intpk]
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    name: Mapped[Optional[str]] = mapped_column(Text, nullable=True, unique=False)
    value: Mapped[Optional[str]] = mapped_column(Text, nullable=True, unique=False)
    date_added: Mapped[created_at]
    date_modified: Mapped[updated_at]
