"""update models persons (add column sex)

Revision ID: d8cd947b9102
Revises: 152f254549f9
Create Date: 2025-04-22 13:57:39.373276

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8cd947b9102'
down_revision: Union[str, None] = '152f254549f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    sex_enum = sa.Enum('FEMALE', 'MALE', name='sex_of_person')
    sex_enum.create(op.get_bind())

    op.add_column('persons', sa.Column('sex', sex_enum, nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('persons', 'sex')

    sex_enum = sa.Enum('FEMALE', 'MALE', name='sex_of_person')
    sex_enum.drop(op.get_bind())
