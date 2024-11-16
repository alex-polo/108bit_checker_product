from typing import Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .annotations import intpk, created_at
from .base import Base


class UrlStatistics(Base):
    __tablename__ = "urls_statistics"

    id: Mapped[intpk]
    internet_site: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, unique=False)
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=False, unique=False)
    status: Mapped[bool]

    date_added: Mapped[created_at]
