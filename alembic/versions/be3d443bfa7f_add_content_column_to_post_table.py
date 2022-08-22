"""add content column to post table

Revision ID: be3d443bfa7f
Revises: 67470639d8db
Create Date: 2022-08-22 17:03:29.943716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be3d443bfa7f'
down_revision = '67470639d8db'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass