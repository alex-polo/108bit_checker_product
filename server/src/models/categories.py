from typing import Optional, List

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import EnableType
from .annotations import intpk, created_at, updated_at
from .base import Base
from .product_to_category import product_to_category


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[intpk]
    parent_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True, unique=False)
    is_enable: Mapped[EnableType] = mapped_column(default=EnableType.disabled)

    internet_site_id: Mapped[Optional[int]] = mapped_column(ForeignKey("internet_sites.id"))
    internet_site: Mapped["InternetSite"] = relationship(back_populates="categories")

    category_image: Mapped[Optional["CategoryImage"]] = relationship(back_populates="category")
    category_description: Mapped["CategoryDescription"] = relationship(back_populates="category")

    products: Mapped[Optional[List["Product"]]] = relationship(secondary=product_to_category,
                                                               back_populates="categories")

    date_added: Mapped[created_at]
    date_modified: Mapped[updated_at]
