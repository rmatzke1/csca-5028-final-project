from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union
from sqlalchemy import Connection
from rmatzke.components.common.mapper_funcs import map_result, map_results
from rmatzke.components.common.templates import DBTemplate


@dataclass
class YoutubeVideoRecord:
    id: int
    youtube_video_id: str
    youtube_channel_id: str
    title: str
    description: str
    publish_date: datetime
    thumbnail_url: str


class YoutubeVideoGateway:
    def __init__(self, db: DBTemplate) -> None:
        self.__db = db

    def list_all(self, limit: int = 50, conn: Optional[Connection] = None) -> List[YoutubeVideoRecord]:
        query = """
            select * from youtube_video
            order by publish_date desc
            limit :limit;
        """
        rows = self.__db.query(statement=query, connection=conn, limit=limit)
        return map_results(
            rows, lambda row: YoutubeVideoRecord(
                id=row["id"],
                youtube_video_id=row["youtube_video_id"],
                youtube_channel_id=row["youtube_channel_id"],
                title=row["title"],
                description=row["description"],
                publish_date=row["publish_date"],
                thumbnail_url=row["thumbnail_url"]
            )
        )

    def insert(
        self,
        youtube_video_id: str,
        youtube_channel_id: str,
        title: str,
        description: str,
        publish_date: datetime,
        thumbnail_url: str,
        conn: Optional[Connection] = None
    ) -> Union[None, YoutubeVideoRecord]:
        query = """
            insert into youtube_video
            (youtube_video_id, youtube_channel_id, title, description, publish_date, thumbnail_url)
            values
            (:youtube_video_id, :youtube_channel_id, :title, :description, :publish_date, :thumbnail_url)
            returning id, youtube_video_id, youtube_channel_id, title, description, publish_date, thumbnail_url;
        """
        result = self.__db.query(
            statement=query,
            connection=conn,
            youtube_video_id=youtube_video_id,
            youtube_channel_id=youtube_channel_id,
            title=title,
            description=description,
            publish_date=publish_date,
            thumbnail_url=thumbnail_url
        )
        return map_result(
            result,
            lambda row: YoutubeVideoRecord(
                id=row["id"],
                youtube_video_id=row["youtube_video_id"],
                youtube_channel_id=row["youtube_channel_id"],
                title=row["title"],
                description=row["description"],
                publish_date=row["publish_date"],
                thumbnail_url=row["thumbnail_url"]
            )
        )

    def get_by_id(self, id: int, conn: Optional[Connection] = None) -> Union[None, YoutubeVideoRecord]:
        query = """
            select * from youtube_video
            where id = :id
            limit 1;
        """
        rows = self.__db.query(statement=query, connection=conn, id=id)
        return map_result(
            rows,
            lambda row: YoutubeVideoRecord(
                id=row["id"],
                youtube_video_id=row["youtube_video_id"],
                youtube_channel_id=row["youtube_channel_id"],
                title=row["title"],
                description=row["description"],
                publish_date=row["publish_date"],
                thumbnail_url=row["thumbnail_url"]
            )
        )
