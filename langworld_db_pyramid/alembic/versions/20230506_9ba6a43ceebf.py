"""add is_multiselect to Feature

Revision ID: 9ba6a43ceebf
Revises: 9df33f0e3069
Create Date: 2023-05-06 20:33:11.917951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ba6a43ceebf'
down_revision = '9df33f0e3069'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('features', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_multiselect', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('features', schema=None) as batch_op:
        batch_op.drop_column('is_multiselect')

    # ### end Alembic commands ###