"""create bibliography table

Revision ID: a001dbc830d9
Revises: 82c00d8df84e
Create Date: 2016-04-23 17:02:30.759629

"""

# revision identifiers, used by Alembic.
revision = 'a001dbc830d9'
down_revision = '82c00d8df84e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'bibliography',
        sa.Column('eid', sa.Unicode(25), primary_key=True),
        sa.Column('bibliography_set_eid', sa.Unicode(25),
                  sa.ForeignKey('bibliography_set.eid')),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('modified', sa.DateTime, nullable=False),
        sa.Column('hash', sa.Unicode(40), nullable=False, index=True),
        sa.Column('title', sa.Unicode(512), nullable=False),
        sa.Column('description', sa.Unicode, nullable=False),
        sa.Column('keywords', sa.Unicode, nullable=False),
        sa.Column('language', sa.Unicode(16), nullable=False),
        sa.Column('full_text_path', sa.Unicode(512), nullable=True),
        sa.UniqueConstraint('bibliography_set_eid', 'hash')
    )


def downgrade():
    op.drop_table('bibliography')
