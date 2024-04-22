"""Add tables Users Tweets Files and one to many users and tweets

Revision ID: 80c9855222f6
Revises: 
Create Date: 2023-09-06 14:12:20.969405

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "80c9855222f6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "files",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("size", sa.Float(), nullable=False),
        sa.Column("extension", sa.String(), nullable=False),
        sa.Column("tweet_ids", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_files_id"), "files", ["id"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("api_key", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("api_key"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "tweets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tweet_data", sa.String(), nullable=False),
        sa.Column(
            "tweet_date_create",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("tweet_has_media", sa.Boolean(), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("archive", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tweets_id"), "tweets", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_tweets_id"), table_name="tweets")
    op.drop_table("tweets")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_files_id"), table_name="files")
    op.drop_table("files")
    # ### end Alembic commands ###