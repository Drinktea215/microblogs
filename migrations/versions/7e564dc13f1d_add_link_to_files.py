"""Add link to files

Revision ID: 7e564dc13f1d
Revises: 43c2188f8a7d
Create Date: 2023-09-23 14:41:13.404534

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7e564dc13f1d"
down_revision = "43c2188f8a7d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("files", sa.Column("link", sa.String()))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("files", "link")
    # ### end Alembic commands ###
