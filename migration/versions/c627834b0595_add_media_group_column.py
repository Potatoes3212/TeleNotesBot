"""Add Media Group column

Revision ID: c627834b0595
Revises: 7e6829ed84ba
Create Date: 2024-12-15 15:36:29.824651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c627834b0595'
down_revision: Union[str, None] = '7e6829ed84ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('reposts', sa.Column('media', postgresql.JSONB(
        astext_type=sa.Text()), nullable=True), schema='reposts')
    op.execute("""
UPDATE reposts.reposts
SET media = jsonb_build_array(
    jsonb_build_object(
        'file_id', file_id,
        'content_type', content_type
    )
)
WHERE file_id IS NOT NULL AND content_type IS NOT NULL;
               """)
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_column('reposts', 'media', schema='reposts')
    # ### end Alembic commands ###
