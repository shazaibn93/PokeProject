"""empty message

Revision ID: 34625b914f82
Revises: aa756b62d697
Create Date: 2022-02-13 23:55:27.356507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34625b914f82'
down_revision = 'aa756b62d697'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('wins', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('losses', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('battles', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'battles')
    op.drop_column('user', 'losses')
    op.drop_column('user', 'wins')
    # ### end Alembic commands ###
