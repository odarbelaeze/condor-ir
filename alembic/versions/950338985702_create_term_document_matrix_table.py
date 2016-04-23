"""create term document matrix table

Revision ID: 950338985702
Revises: a001dbc830d9
Create Date: 2016-04-23 17:21:18.745499

"""

# revision identifiers, used by Alembic.
revision = '950338985702'
down_revision = 'a001dbc830d9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'term_document_matrix',
        sa.Column('eid', sa.Unicode(25), primary_key=True),
        sa.Column('bibliography_set_eid', sa.Unicode(25),
                  sa.ForeignKey('bibliography_set.eid')),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('modified', sa.DateTime, nullable=False),
        sa.Column('bibliography_options', sa.Unicode(512), nullable=False),
        sa.Column('processing_options', sa.Unicode(512), nullable=False),
        sa.Column('term_list_path', sa.Unicode(512), nullable=False),
        sa.Column('tdidf_matrix_path', sa.Unicode(512), nullable=False),
    )


def downgrade():
    op.drop_table('term_document_matrix')
