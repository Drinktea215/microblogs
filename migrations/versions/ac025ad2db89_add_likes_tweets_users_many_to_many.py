"""Add likes tweets users - many to many

Revision ID: ac025ad2db89
Revises: 80c9855222f6
Create Date: 2023-09-06 14:18:10.712964

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ac025ad2db89"
down_revision = "80c9855222f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "assoc_table_for_likes",
        sa.Column("tweet_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tweet_id"], ["tweets.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("tweet_id", "user_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("assoc_table_for_likes")
    # ### end Alembic commands ###
