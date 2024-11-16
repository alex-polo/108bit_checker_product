from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .annotations import intpk, created_at, updated_at
from .base import Base


class ProductDocument(Base):
    __tablename__ = "products_documents"

    id: Mapped[intpk]
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    document: Mapped["Storage"] = relationship(back_populates="product_document")
    name: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True, unique=False)
    date_added: Mapped[created_at]
    date_modified: Mapped[updated_at]

