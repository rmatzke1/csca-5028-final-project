from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Connection
from typing import Optional, Union
from rmatzke.components.common.mapper_funcs import map_result
from rmatzke.components.common.templates import DBTemplate


@dataclass
class CollectorRunRecord:
    id: int
    run_start: datetime
    run_end: datetime
    param_published_before: datetime
    param_published_after: datetime
    video_count: int


class CollectorRunGateway:
    def __init__(self, db: DBTemplate) -> None:
        self.__db = db

    def insert(
        self,
        run_start: datetime,
        run_end: datetime,
        param_published_before: datetime,
        param_published_after: datetime,
        video_count: int,
        conn: Optional[Connection] = None,
    ) -> None:
        query = """
            insert into collector_run
            (run_start, run_end, param_published_before, param_published_after, video_count)
            values
            (:run_start, :run_end, :param_published_before, :param_published_after, :video_count);
        """
        self.__db.query(
            statement=query,
            connection=conn,
            run_start=run_start,
            run_end=run_end,
            param_published_before=param_published_before,
            param_published_after=param_published_after,
            video_count=video_count,
        )

    def get_latest(self, conn: Optional[Connection] = None) -> Union[None, CollectorRunRecord]:
        query = """
            select * from collector_run
            order by param_published_before desc
            limit 1;
        """
        result = self.__db.query(statement=query, connection=conn)
        return map_result(
            result,
            lambda row: CollectorRunRecord(
                id=row["id"],
                run_start=row["run_start"],
                run_end=row["run_end"],
                param_published_before=row["param_published_before"],
                param_published_after=row["param_published_after"],
                video_count=row["video_count"],
            ),
        )
