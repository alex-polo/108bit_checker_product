"""Database change

Revision ID: e4c4429366c5
Revises: 228477e4f392
Create Date: 2024-11-16 18:20:53.887347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4c4429366c5'
down_revision: Union[str, None] = '228477e4f392'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_category108bit_id', table_name='categories_108bit')
    op.drop_index('idx_manufacturer_name', table_name='manufacturers')
    op.drop_index('idx_product_to_category_category_id', table_name='product_to_category_108bit')
    op.drop_index('idx_product_to_category_product_id', table_name='product_to_category_108bit')
    op.add_column('products', sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True))
    op.drop_index('idx_product_manufacturer_id', table_name='products')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_product_manufacturer_id', 'products', ['manufacturer_id'], unique=False)
    op.drop_column('products', 'price')
    op.create_index('idx_product_to_category_product_id', 'product_to_category_108bit', ['product_id'], unique=False)
    op.create_index('idx_product_to_category_category_id', 'product_to_category_108bit', ['category_id'], unique=False)
    op.create_index('idx_manufacturer_name', 'manufacturers', ['name'], unique=False)
    op.create_index('idx_category108bit_id', 'categories_108bit', ['id'], unique=False)
    # ### end Alembic commands ###