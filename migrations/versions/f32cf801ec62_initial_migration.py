"""Initial Migration

Revision ID: f32cf801ec62
Revises: c1180bb9d90f
Create Date: 2021-06-20 23:26:48.445342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f32cf801ec62'
down_revision = 'c1180bb9d90f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('posted', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'posted')
    # ### end Alembic commands ###