"""empty message

Revision ID: ee2ad51bbc34
Revises: 25ce8bd47576
Create Date: 2024-03-27 16:37:55.033373

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ee2ad51bbc34'
down_revision = '25ce8bd47576'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rifa', schema=None) as batch_op:
        batch_op.alter_column('id_pessoa',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rifa', schema=None) as batch_op:
        batch_op.alter_column('id_pessoa',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)

    # ### end Alembic commands ###
