"""Add one to many tweets and files

Revision ID: c597ba20a8fa
Revises: 2932ae0309bd
Create Date: 2023-09-21 22:34:21.432987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c597ba20a8fa'
down_revision = '2932ae0309bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('files', 'tweet_ids',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'files', 'tweets', ['tweet_ids'], ['id'])
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'files', type_='foreignkey')
    op.alter_column('files', 'tweet_ids',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
