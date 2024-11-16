from typing import Optional, List

from sqlalchemy import String, ForeignKey, Text, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .annotations import intpk, created_at, updated_at, string_256
from .enum_types import EnableType
from .base import Base
from .product_to_category import product_to_category
from .product_to_category_108bit import product_to_category_108bit

class Product(Base):
    __tablename__ = "products"

    id: Mapped[intpk]

    categories: Mapped[List["Category"]] = relationship(secondary=product_to_category, back_populates="products")
    categories_108bit: Mapped[List["Category108BIT"]] = relationship(secondary=product_to_category_108bit,
                                                                      back_populates="products")

    equipment_line = relationship('EquipmentLines', back_populates='products')

    manufacturer_id: Mapped[Optional[int]] = mapped_column(ForeignKey("manufacturers.id"))
    manufacturer: Mapped[Optional["Manufacturer"]] = relationship(back_populates="products")

    product_description: Mapped["ProductDescription"] = relationship(back_populates="product")

    article: Mapped[Optional[string_256]] = mapped_column(unique=False)
    article_2: Mapped[Optional[string_256]] = mapped_column(unique=False)

    quantity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, unique=False)
    price: Mapped[Optional[int]] = mapped_column(Numeric(10, 2), nullable=True, unique=False)

    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True, unique=False)
    is_enable: Mapped[EnableType] = mapped_column(default=EnableType.disabled)

    avito_sellers: Mapped[List["AvitoSeller"]] = relationship()

    attributes: Mapped[List["ProductAttribute"]] = relationship()
    images: Mapped[List["ProductImage"]] = relationship()
    documents: Mapped[List["ProductDocument"]] = relationship()

    date_added: Mapped[created_at]
    date_modified: Mapped[updated_at]

