"""Add followers

Revision ID: 9563d964bae0
Revises: ac025ad2db89
Create Date: 2023-09-08 14:41:16.419584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9563d964bae0'
down_revision = 'ac025ad2db89'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
