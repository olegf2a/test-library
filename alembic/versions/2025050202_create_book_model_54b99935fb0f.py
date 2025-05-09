"""create_book_model

Revision ID: 54b99935fb0f
Revises:
Create Date: 2025-05-02 18:02:37.914257

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "54b99935fb0f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "book",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("author", sa.String(length=256), nullable=False),
        sa.Column("genre", sa.String(length=256), nullable=False),
        sa.Column("date_published", sa.Date(), nullable=False),
        sa.Column("file_path", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_book_author"), "book", ["author"], unique=False)
    op.create_index(op.f("ix_book_genre"), "book", ["genre"], unique=False)
    op.create_index(op.f("ix_book_name"), "book", ["name"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_book_name"), table_name="book")
    op.drop_index(op.f("ix_book_genre"), table_name="book")
    op.drop_index(op.f("ix_book_author"), table_name="book")
    op.drop_table("book")
    # ### end Alembic commands ###
