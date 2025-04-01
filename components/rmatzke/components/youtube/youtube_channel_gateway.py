from dataclasses import dataclass
from typing import List, Optional
from sqlalchemy import Connection
from rmatzke.components.common.mapper_funcs import map_results
from rmatzke.components.common.templates import DBTemplate


@dataclass
class YoutubeChannelRecord:
    id: int
    handle: str


class YoutubeChannelGateway:
    def __init__(self, db: DBTemplate) -> None:
        self.__db = db

    def list_all(self, conn: Optional[Connection] = None) -> List[YoutubeChannelRecord]:
        query = """
            select * from youtube_channel;
        """
        result = self.__db.query(statement=query, connection=conn)
        return map_results(
            result, lambda row: YoutubeChannelRecord(id=row["id"], handle=row["handle"])
        )
