from typing import Optional

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .annotations import intpk, created_at, updated_at
from .base import Base

class EquipmentLines(Base):
    __tablename__ = "equipment_lines"

    id: Mapped[intpk]
    name: Mapped[Optional[str]] = mapped_column(Text, nullable=False, unique=False)

    # Внешний ключ, указывающий на родителя
    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey("products.id"))
    products = relationship('Product', back_populates='equipment_line')  # Обратная связь

    date_added: Mapped[created_at]
    date_modified: Mapped[updated_at]
