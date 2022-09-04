"""split comment column in Doculect in two (1 per locale)

Revision ID: 246890497aa1
Revises: b65301860518
Create Date: 2022-06-22 13:29:15.686304

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '246890497aa1'
down_revision = 'b65301860518'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('doculects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment_en', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('comment_ru', sa.Text(), nullable=True))
        batch_op.drop_column('comment')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('doculects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment', sa.TEXT(), nullable=True))
        batch_op.drop_column('comment_ru')
        batch_op.drop_column('comment_en')

    # ### end Alembic commands ###
