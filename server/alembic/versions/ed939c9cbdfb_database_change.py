"""Database change

Revision ID: ed939c9cbdfb
Revises: eba29d76d2ac
Create Date: 2024-11-12 18:39:36.280224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed939c9cbdfb'
down_revision: Union[str, None] = 'eba29d76d2ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('equipment_lines_name_key', 'equipment_lines', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('equipment_lines_name_key', 'equipment_lines', ['name'])
    # ### end Alembic commands ###