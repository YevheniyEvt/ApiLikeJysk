"""drop all table

Revision ID: 10bbe8593449
Revises: 56152ede8e8d
Create Date: 2025-01-25 12:12:04.788363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10bbe8593449'
down_revision: Union[str, None] = '56152ede8e8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('ticket')
    op.drop_table('task')
    op.drop_table('news')
    op.drop_table('competition')
    op.drop_table('employee')
    op.drop_table('store')
    op.drop_table('store_position')
    op.drop_table('retail_position')
    op.drop_table('region')
    op.drop_table('office_department')
    op.drop_table('location')
    op.drop_table('district')
    op.drop_table('country')


def downgrade() -> None:
    pass
