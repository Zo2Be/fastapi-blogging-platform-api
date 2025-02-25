"""Create categories table

Revision ID: 8e5ef7edeed4
Revises: 7d147b1fc5ec
Create Date: 2025-02-19 19:37:17.319957

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8e5ef7edeed4"
down_revision: Union[str, None] = "7d147b1fc5ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=15), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_categories")),
        sa.UniqueConstraint("name", name=op.f("uq_categories_name")),
    )


def downgrade() -> None:
    op.drop_table("categories")
