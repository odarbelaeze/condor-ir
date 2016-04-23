"""create query result table

Revision ID: 5ceb3aac961e
Revises: 3da7a1f98866
Create Date: 2016-04-23 18:19:58.987849

"""

# revision identifiers, used by Alembic.
revision = '5ceb3aac961e'
down_revision = '3da7a1f98866'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'query_result',
        sa.Column('eid', sa.Unicode(25), primary_key=True),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('modified', sa.DateTime, nullable=False),
        sa.Column('query_eid', sa.Unicode(25),
                  sa.ForeignKey('query.eid')),
        sa.Column('bibliography_eid', sa.Unicode(25),
                  sa.ForeignKey('bibliography.eid')),
    )


def downgrade():
    op.drop_table('query_result')
