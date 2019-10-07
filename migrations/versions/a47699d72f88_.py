"""empty message

Revision ID: a47699d72f88
Revises: 949fc6c95296
Create Date: 2019-10-07 11:02:25.366587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a47699d72f88'
down_revision = '949fc6c95296'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('facebook', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'facebook')
    # ### end Alembic commands ###