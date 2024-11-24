"""Create schemas

Revision ID: f0660caf9d2f
Revises: 15f71d675cee
Create Date: 2024-11-21 20:50:29.266669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0660caf9d2f'
down_revision: Union[str, None] = '15f71d675cee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создание новых схем
    op.execute("CREATE SCHEMA IF NOT EXISTS users")
    op.execute("CREATE SCHEMA IF NOT EXISTS notes")
    op.execute("CREATE SCHEMA IF NOT EXISTS reposts")

def downgrade():
    # Удаление схем в случае отката (если необходимо)
    op.execute("DROP SCHEMA IF EXISTS users CASCADE")
    op.execute("DROP SCHEMA IF EXISTS notes CASCADE")
    op.execute("DROP SCHEMA IF EXISTS reposts CASCADE")