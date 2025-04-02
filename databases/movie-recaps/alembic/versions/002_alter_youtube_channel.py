"""alter youtube_channel

Revision ID: 002
Revises: 001
Create Date: 2025-04-01 15:06:03.181722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        alter table youtube_channel
        add column youtube_channel_id varchar(255) unique;
        """
    )


def downgrade() -> None:
    op.exec(
        """
        alter table youtube_channel_id
        drop column youtube_id;
        """
    )
