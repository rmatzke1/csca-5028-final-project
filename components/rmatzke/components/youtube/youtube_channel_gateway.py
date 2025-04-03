from dataclasses import dataclass
from typing import List, Optional
from sqlalchemy import Connection
from rmatzke.components.common.mapper_funcs import map_results
from rmatzke.components.common.templates import DBTemplate


@dataclass
class YoutubeChannelRecord:
    id: int
    youtube_handle: str
    youtube_channel_id: str


class YoutubeChannelGateway:
    def __init__(self, db: DBTemplate) -> None:
        self.__db = db

    def list_all(self, conn: Optional[Connection] = None) -> List[YoutubeChannelRecord]:
        query = """
            select * from youtube_channel;
        """
        rows = self.__db.query(statement=query, connection=conn)
        return map_results(
            rows, lambda row: YoutubeChannelRecord(
                id=row["id"],
                youtube_handle=row["youtube_handle"],
                youtube_channel_id=row["youtube_channel_id"]
            )
        )

    def list_with_channel_ids(self, conn: Optional[Connection] = None) -> List[YoutubeChannelRecord]:
        query = """
            select * from youtube_channel
            where youtube_channel_id is not null;
        """
        rows = self.__db.query(statement=query, connection=conn)
        return map_results(
            rows, lambda row: YoutubeChannelRecord(
                id=row["id"],
                youtube_handle=row["youtube_handle"],
                youtube_channel_id=row["youtube_channel_id"]
            )
        )

    def list_without_channel_ids(self, conn: Optional[Connection] = None) -> List[YoutubeChannelRecord]:
        query = """
            select * from youtube_channel
            where youtube_channel_id is null;
        """
        rows = self.__db.query(statement=query, connection=conn)
        return map_results(
            rows, lambda row: YoutubeChannelRecord(
                id=row["id"],
                youtube_handle=row["youtube_handle"],
                youtube_channel_id=row["youtube_channel_id"]
            )
        )

    def set_channel_id(self, id: int, youtube_channel_id: str, conn: Optional[Connection] = None) -> None:
        query = """
            update youtube_channel
            set youtube_channel_id = :youtube_channel_id
            where id = :id;
        """
        self.__db.query(
            statement=query,
            connection=conn,
            youtube_channel_id=youtube_channel_id,
            id=id
        )
