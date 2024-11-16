from typing import Optional, List

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enum_types import EnableType
from .annotations import intpk, created_at, updated_at
from .base import Base
from .product_to_category_108bit import product_to_category_108bit


class Category108BIT(Base):
    __tablename__ = "categories_108bit"

    id: Mapped[intpk]
    parent_id: Mapped[int] = mapped_column(ForeignKey('categories_108bit.id'), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True, unique=False)
    is_enable: Mapped[EnableType] = mapped_column(default=EnableType.disabled)

    internet_site_id: Mapped[Optional[int]] = mapped_column(ForeignKey("internet_sites.id"))
    internet_site: Mapped["InternetSite"] = relationship(back_populates="categories_108bit")

    title: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True, unique=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, unique=False)

    products: Mapped[Optional[List["Product"]]] = relationship(secondary=product_to_category_108bit,
                                                               back_populates="categories_108bit")

    date_added: Mapped[created_at]
    date_modified: Mapped[updated_at]
