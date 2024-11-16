from typing import Optional

from sqlalchemy import ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .annotations import intpk, created_at, updated_at
from .base import Base


class Storage(Base):
    __tablename__ = "storage"

    id: Mapped[intpk]
    folder: Mapped[str] = mapped_column(String(4096), nullable=True, unique=False)
    filename: Mapped[str] = mapped_column(String(4096), nullable=True, unique=False)
    uuid: Mapped[UUID] = mapped_column(UUID(), nullable=True, unique=True)

    product_image_id: Mapped[int] = mapped_column(ForeignKey("products_images.id"), nullable=True)
    product_image: Mapped[Optional["ProductImage"]] = relationship(back_populates="image")

    product_document_id: Mapped[int] = mapped_column(ForeignKey("products_documents.id"), nullable=True)
    product_document: Mapped[Optional["ProductDocument"]] = relationship(back_populates="document")

    category_image_id: Mapped[int] = mapped_column(ForeignKey("category_images.id"), nullable=True)
    category_image: Mapped[Optional["CategoryImage"]] = relationship(back_populates="image")

    date_added: Mapped[created_at]
    date_modified: Mapped[updated_at]
