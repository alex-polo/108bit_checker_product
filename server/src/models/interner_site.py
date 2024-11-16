from typing import Optional, List

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .annotations import intpk, created_at, updated_at
from .base import Base

class InternetSite(Base):
    __tablename__ = "internet_sites"

    id: Mapped[intpk]
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=False, unique=True)
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True, unique=False)
    categories: Mapped[Optional[List["Category"]]] = relationship(back_populates='internet_site')
    categories_108bit: Mapped[Optional[List["Category108BIT"]]] = relationship(back_populates='internet_site')
    date_added: Mapped[created_at]
    date_modified: Mapped[updated_at]
