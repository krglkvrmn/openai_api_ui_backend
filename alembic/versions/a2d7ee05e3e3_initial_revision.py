"""Initial revision

Revision ID: a2d7ee05e3e3
Revises: 
Create Date: 2023-09-09 22:51:24.378224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a2d7ee05e3e3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('chats')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('chats_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('model', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('last_updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='chats_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('messages',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('author', postgresql.ENUM('user', 'assistant', 'system', name='author'), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('chat_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], name='messages_chat_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='messages_pkey')
    )
    # ### end Alembic commands ###