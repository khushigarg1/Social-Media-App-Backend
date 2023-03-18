"""add title and content column to socialmediapost table

Revision ID: 56a13f2100b9
Revises: 01fc5e6c4ed2
Create Date: 2023-03-02 12:14:52.118292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56a13f2100b9'
down_revision = '01fc5e6c4ed2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('socialmediapost', sa.Column(
        'title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('socialmediapost', 'title')
    pass
