"""add video tables

Revision ID: 003
Revises: 002
Create Date: 2025-04-01 18:57:49.907697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        create table genre (
            id serial primary key,
            genre varchar(255) not null unique
        );

        insert into genre (genre) values
            ('Action'),
            ('Adventure'),
            ('Comedy'),
            ('Crime'),
            ('Documentary'),
            ('Drama'),
            ('Fantasy'),
            ('Horror'),
            ('Mystery'),
            ('Romance'),
            ('Science Fiction'),
            ('Thriller'),
            ('War'),
            ('Western');

        create table youtube_video (
            id serial primary key,
            youtube_video_id varchar(255) not null unique,
            youtube_channel_id varchar(255) not null,
            title varchar(255) not null,
            description varchar(255),
            publish_date timestamp not null,
            thumbnail_url varchar(255)
        );
        
        create table youtube_video_genre (
            id serial primary key,
            genre_id int not null,
            youtube_video_id int not null
        );
        """
    )


def downgrade() -> None:
    op.execute(
        """
        drop table if exists youtube_video_genre;
        drop table if exists youtube_video;
        drop table if exists genre;
        """
    )
