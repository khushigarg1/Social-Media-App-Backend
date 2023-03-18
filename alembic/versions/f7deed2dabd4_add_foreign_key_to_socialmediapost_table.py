"""add foreign-key to socialmediapost table

Revision ID: f7deed2dabd4
Revises: 29bd7b58443f
Create Date: 2023-03-02 13:22:29.094419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7deed2dabd4'
down_revision = '29bd7b58443f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('socialmediapost', sa.Column(
        'owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('socialmediapost_users_fk', source_table="socialmediapost",
                          referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('socialmediapost_users_fk',
                       table_name="socialmediapost")
    op.drop_column('socialmediapost', 'owner_id')
    pass
