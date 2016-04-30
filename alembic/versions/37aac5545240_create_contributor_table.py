"""create contributor table

Revision ID: 37aac5545240
Revises: 5d2851b90057
Create Date: 2016-04-23 17:59:57.155034

"""

# revision identifiers, used by Alembic.
revision = '37aac5545240'
down_revision = '5d2851b90057'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'contributor',
        sa.Column('eid', sa.Unicode(40), primary_key=True),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('modified', sa.DateTime, nullable=False),
        sa.Column('name', sa.Unicode(512), nullable=False),
        sa.Column('email', sa.Unicode(512), nullable=False, index=True),
        sa.Column('language', sa.Unicode(16), nullable=False),
        sa.Column('topics', sa.Unicode(512), nullable=False),
    )


def downgrade():
    op.drop_table('contributor')
