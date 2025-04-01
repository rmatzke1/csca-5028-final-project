"""init

Revision ID: 001
Revises: 
Create Date: 2025-03-28 08:20:44.047427

"""
import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        create table youtube_channel (
            id serial primary key,
            handle varchar(255) not null unique
        );

        insert into youtube_channel (handle) values
            ('movierecapsofficial'),
            ('mysteryrecappedofficial'),
            ('themovierecapofficial'),
            ('todaysrecapmovie'),
            ('filmrecapshere'),
            ('moviesoutpost'),
            ('manofrecaps'),
            ('minutemovies1'),
            ('storyflixmovierecap'),
            ('recapkingofficial');
        
        create table collector_run (
            id serial primary key,
            run_start timestamp,
            run_end timestamp,
            param_published_before timestamp not null,
            param_published_after timestamp not null,
            video_count int not null
        );
        """
    )


def downgrade() -> None:
    pass
