"""Add APIKey table

Revision ID: ee684b23162c
Revises: 1d53b317bbf0
Create Date: 2023-12-18 00:16:20.065782

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee684b23162c'
down_revision: Union[str, None] = '1d53b317bbf0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_key',
    sa.Column('id', sa.UUID(), nullable=False, default=uuid.uuid4),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('api_key')
    # ### end Alembic commands ###