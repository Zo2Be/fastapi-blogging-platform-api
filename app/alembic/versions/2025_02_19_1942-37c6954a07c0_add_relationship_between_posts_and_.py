"""Add relationship between posts and categories

Revision ID: 37c6954a07c0
Revises: 8e5ef7edeed4
Create Date: 2025-02-19 19:42:24.760719

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "37c6954a07c0"
down_revision: Union[str, None] = "8e5ef7edeed4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("category_id", sa.Integer(), nullable=False))
    op.create_index(
        op.f("ix_posts_category_id"), "posts", ["category_id"], unique=False
    )
    op.create_foreign_key(
        op.f("fk_posts_category_id_categories"),
        "posts",
        "categories",
        ["category_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_posts_category_id_categories"), "posts", type_="foreignkey"
    )
    op.drop_index(op.f("ix_posts_category_id"), table_name="posts")
    op.drop_column("posts", "category_id")
