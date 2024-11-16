from sqlalchemy import Table, Column, ForeignKey

from .base import Base

product_to_category = Table(
    "product_to_category",

    Base.metadata,
    Column("product_id", ForeignKey("products.id")),
    Column("category_id", ForeignKey("categories.id")),
)