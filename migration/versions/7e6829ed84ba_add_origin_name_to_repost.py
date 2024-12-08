"""Add origin_name to Repost

Revision ID: 7e6829ed84ba
Revises: dcaa277b8b46
Create Date: 2024-12-01 20:08:42.776050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e6829ed84ba'
down_revision: Union[str, None] = 'dcaa277b8b46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('reposts', sa.Column('origin_name', sa.String(), nullable=True), schema='reposts')
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_column('reposts','origin_name', schema='reposts')
    # ### end Alembic commands ###
