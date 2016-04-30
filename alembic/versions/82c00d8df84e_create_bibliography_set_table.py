"""create bibliography set table

Revision ID: 82c00d8df84e
Revises:
Create Date: 2016-04-23 16:56:09.581645

"""

# revision identifiers, used by Alembic.
revision = '82c00d8df84e'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'bibliography_set',
        sa.Column('eid', sa.Unicode(40), primary_key=True),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('modified', sa.DateTime, nullable=False),
        sa.Column('description', sa.Unicode, nullable=False),
    )


def downgrade():
    op.drop_table('bibliography_set')
