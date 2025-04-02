from dataclasses import dataclass
from typing import List, Optional, Union
from sqlalchemy import Connection
from rmatzke.components.common.mapper_funcs import map_result
from rmatzke.components.common.templates import DBTemplate


@dataclass
class YoutubeVideoRecord:
    id: int
    youtube_video_id: str
    youtube_channel_id: str
    title: str
    description: str


class YoutubeVideoGateway:
    def __init__(self, db: DBTemplate) -> None:
        self.__db = db

    def insert(
        self,
        youtube_video_id: str,
        youtube_channel_id: str,
        title: str,
        description: str,
        conn: Optional[Connection] = None,
    ) -> Union[None, YoutubeVideoRecord]:
        query = """
            insert into youtube_video
            (youtube_video_id, youtube_channel_id, title, description)
            values
            (:youtube_video_id, :youtube_channel_id, :title, :description)
            returning id, youtube_video_id, youtube_channel_id, title, description;
        """
        result = self.__db.query(
            statement=query,
            connection=conn,
            youtube_video_id=youtube_video_id,
            youtube_channel_id=youtube_channel_id,
            title=title,
            description=description
        )
        return map_result(
            result,
            lambda row: YoutubeVideoRecord(
                id=row["id"],
                youtube_video_id=row["youtube_video_id"],
                youtube_channel_id=row["youtube_channel_id"],
                title=row["title"],
                description=row["description"]
            )
        )
