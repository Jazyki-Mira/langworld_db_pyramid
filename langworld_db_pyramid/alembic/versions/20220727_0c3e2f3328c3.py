"""add column  to FeatureValue


Revision ID: 0c3e2f3328c3
Revises: bef39c85c32b
Create Date: 2022-07-27 14:45:44.236959

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0c3e2f3328c3'
down_revision = 'bef39c85c32b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feature_values', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_listed_and_has_doculects', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feature_values', schema=None) as batch_op:
        batch_op.drop_column('is_listed_and_has_doculects')

    # ### end Alembic commands ###
