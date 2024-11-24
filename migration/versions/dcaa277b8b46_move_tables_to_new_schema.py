"""Move tables to new schema

Revision ID: dcaa277b8b46
Revises: f0660caf9d2f
Create Date: 2024-11-21 20:54:44.037838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dcaa277b8b46'
down_revision: Union[str, None] = 'f0660caf9d2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Перемещение таблиц в новые схемы
    op.execute("ALTER TABLE public.users SET SCHEMA users")
    op.execute("ALTER TABLE public.notes SET SCHEMA notes")
    op.execute("ALTER TABLE public.reposts SET SCHEMA reposts")

def downgrade():
    # Перемещение таблиц обратно в схему public
    op.execute("ALTER TABLE users.users SET SCHEMA public")
    op.execute("ALTER TABLE notes.notes SET SCHEMA public")
    op.execute("ALTER TABLE reposts.reposts SET SCHEMA public")