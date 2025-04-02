from dataclasses import dataclass
from typing import List, Optional
from sqlalchemy import Connection
from rmatzke.components.common.mapper_funcs import map_results
from rmatzke.components.common.templates import DBTemplate


@dataclass
class YoutubeVideoGenreRecord:
    id: int
    genre_id: int
    youtube_video_id: int


class YoutubeVideoGenreGateway:
    def __init__(self, db: DBTemplate) -> None:
        self.__db = db

    def insert(
        self,
        genre_id: int,
        youtube_video_id: int,
        conn: Optional[Connection] = None,
    ) -> None:
        query = """
            insert into youtube_video_genre
            (genre_id, youtube_video_id)
            values
            (:genre_id, :youtube_video_id);
        """
        self.__db.query(
            statement=query,
            connection=conn,
            genre_id=genre_id,
            youtube_video_id=youtube_video_id
        )
