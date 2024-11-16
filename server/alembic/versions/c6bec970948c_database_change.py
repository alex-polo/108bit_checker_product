"""Database change

Revision ID: c6bec970948c
Revises: 905fae34ce59
Create Date: 2024-11-16 19:37:46.047504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6bec970948c'
down_revision: Union[str, None] = '905fae34ce59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'storage', ['uuid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'storage', type_='unique')
    # ### end Alembic commands ###