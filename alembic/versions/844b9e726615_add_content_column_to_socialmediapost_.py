"""add content column to socialmediapost table

Revision ID: 844b9e726615
Revises: 56a13f2100b9
Create Date: 2023-03-02 12:28:01.887887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '844b9e726615'
down_revision = '56a13f2100b9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('socialmediapost', sa.Column(
        'content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('socialmediapost', 'content')
    pass
