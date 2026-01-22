"""create phone number for user column

Revision ID: 1f5415e7789d
Revises:
Create Date: 2026-01-22 13:38:08.397188

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1f5415e7789d"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("phone_number", sa.String(length=9), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
