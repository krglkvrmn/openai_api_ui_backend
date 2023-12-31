"""Added connection between chat and user

Revision ID: 123a89d3834f
Revises: a6862bc18c12
Create Date: 2023-12-02 15:44:30.526445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '123a89d3834f'
down_revision: Union[str, None] = 'a6862bc18c12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('user_id', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'chats', 'user', ['user_id'], ['id'])
    op.alter_column('system_prompt', 'content',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('system_prompt', 'popularity',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('system_prompt', 'popularity',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('system_prompt', 'content',
               existing_type=sa.TEXT(),
               nullable=False)
    op.drop_constraint(None, 'chats', type_='foreignkey')
    op.drop_column('chats', 'user_id')
    # ### end Alembic commands ###
