"""add last few columns  to socialmediapost table

Revision ID: 1592d6a310f8
Revises: f7deed2dabd4
Create Date: 2023-03-02 13:48:13.706554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1592d6a310f8'
down_revision = 'f7deed2dabd4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('socialmediapost', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('socialmediapost', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('NOW()')),)

    pass


def downgrade():
    op.drop_column('socialmediapost', 'published')
    op.drop_column('socialmediapost', 'created_at')
    pass
