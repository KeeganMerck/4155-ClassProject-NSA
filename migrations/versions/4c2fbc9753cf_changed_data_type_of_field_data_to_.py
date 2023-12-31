"""Changed data type of field data to Integer in StackEntry

Revision ID: 4c2fbc9753cf
Revises: 9961f3fb1ace
Create Date: 2023-11-15 18:51:32.888922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c2fbc9753cf'
down_revision = '9961f3fb1ace'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stack_entry', schema=None) as batch_op:
        batch_op.alter_column('data',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stack_entry', schema=None) as batch_op:
        batch_op.alter_column('data',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)

    # ### end Alembic commands ###
