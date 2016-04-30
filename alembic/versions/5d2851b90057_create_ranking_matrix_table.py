"""create ranking matrix table

Revision ID: 5d2851b90057
Revises: 950338985702
Create Date: 2016-04-23 17:32:37.781359

"""

# revision identifiers, used by Alembic.
revision = '5d2851b90057'
down_revision = '950338985702'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'ranking_matrix',
        sa.Column('eid', sa.Unicode(40), primary_key=True),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('modified', sa.DateTime, nullable=False),
        sa.Column('term_document_matrix_eid', sa.Unicode(40),
                  sa.ForeignKey('term_document_matrix.eid')),
        sa.Column('type', sa.Unicode(16), nullable=False),
        sa.Column('build_options', sa.Unicode(512), nullable=False),
        sa.Column('ranking_matrix_path', sa.Unicode(512), nullable=False),
    )


def downgrade():
    op.drop_table('ranking_matrix')
