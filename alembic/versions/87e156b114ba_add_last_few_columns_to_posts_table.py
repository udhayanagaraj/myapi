"""add last few columns to posts table

Revision ID: 87e156b114ba
Revises: c722ab000ecb
Create Date: 2022-08-22 17:19:31.291725

"""
from http import server
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87e156b114ba'
down_revision = 'c722ab000ecb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column("posts",'published')
    op.drop_column("posts",'created_at')
    pass
