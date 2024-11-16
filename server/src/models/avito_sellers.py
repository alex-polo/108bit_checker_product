from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .annotations import intpk, created_at, updated_at
from .base import Base


class AvitoSeller(Base):
    __tablename__ = "avito_sellers"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[Optional[str]] = mapped_column(String(2056))
    url: Mapped[str] = mapped_column(String(4096))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    date_added: Mapped[created_at]
    date_modified: Mapped[updated_at]
