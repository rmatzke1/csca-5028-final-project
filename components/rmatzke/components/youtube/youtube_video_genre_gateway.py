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

    def list_by_youtube_video_id(self, youtube_video_id: int, conn: Optional[Connection] = None) -> List[YoutubeVideoGenreRecord]:
        query = """
            select * from youtube_video_genre
            where youtube_video_id = :youtube_video_id;
        """
        rows = self.__db.query(statement=query, connection=conn, youtube_video_id=youtube_video_id)
        return map_results(
            rows, lambda row: YoutubeVideoGenreRecord(
                id=row["id"],
                genre_id=row["genre_id"],
                youtube_video_id=row["youtube_video_id"]
            )
        )

    def list_by_genre_id(self, genre_id: int, conn: Optional[Connection] = None) -> List[YoutubeVideoGenreRecord]:
        query = """
            select * from youtube_video_genre
            where genre_id = :genre_id;
        """
        rows = self.__db.query(statement=query, connection=conn, genre_id=genre_id)
        return map_results(
            rows, lambda row: YoutubeVideoGenreRecord(
                id=row["id"],
                genre_id=row["genre_id"],
                youtube_video_id=row["youtube_video_id"]
            )
        )
