"""create socialmediapost tables

Revision ID: 01fc5e6c4ed2
Revises: 834385dfa4e3
Create Date: 2023-03-02 01:16:25.985284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01fc5e6c4ed2'
down_revision = None
branch_labels = None
depends_on = None


# ------if we want to create a table then we ahve to write all logic in upgrade table iff want to change or modify then in downgrade table fi soemthing messed up
def upgrade():
    op.create_table('socialmediapost', sa.Column(
        'id', sa.Integer(), nullable=False, primary_key=True))
    pass


def downgrade():
    # op.drop_table('socialmediapost')
    pass
