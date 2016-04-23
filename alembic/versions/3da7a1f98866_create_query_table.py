"""create query table

Revision ID: 3da7a1f98866
Revises: 37aac5545240
Create Date: 2016-04-23 18:05:13.390063

"""

# revision identifiers, used by Alembic.
revision = '3da7a1f98866'
down_revision = '37aac5545240'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'query',
        sa.Column('eid', sa.Unicode(25), primary_key=True),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('modified', sa.DateTime, nullable=False),
        sa.Column('contributor_eid', sa.Unicode(25),
                  sa.ForeignKey('contributor.eid')),
        sa.Column('bibliography_set_eid', sa.Unicode(25),
                  sa.ForeignKey('bibliography_set.eid')),
        sa.Column('query_string', sa.Unicode(1024), nullable=False),
    )


def downgrade():
    op.drop_table('query')
