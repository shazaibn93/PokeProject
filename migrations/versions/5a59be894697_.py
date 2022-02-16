"""empty message

Revision ID: 5a59be894697
Revises: 8428a10685f3
Create Date: 2022-02-08 22:39:25.497632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a59be894697'
down_revision = '8428a10685f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('caughtem',
    sa.Column('pokeid', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pokeid'], ['poketeam.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('pokeid', 'userid')
    )
    op.drop_table('caught')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('caught',
    sa.Column('squad_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['squad_id'], ['user.id'], name='caught_squad_id_fkey')
    )
    op.drop_table('caughtem')
    # ### end Alembic commands ###
