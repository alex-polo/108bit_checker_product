from sqlalchemy import Table, Column, ForeignKey

from .base import Base

product_to_category_108bit = Table(
    "product_to_category_108bit",

    Base.metadata,
    Column("product_id", ForeignKey("products.id")),
    Column("category_id", ForeignKey("categories_108bit.id")),
)