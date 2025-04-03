from dataclasses import dataclass
from typing import List, Optional, Union
from sqlalchemy import Connection
from rmatzke.components.common.mapper_funcs import map_result, map_results
from rmatzke.components.common.templates import DBTemplate


@dataclass
class GenreRecord:
    id: int
    genre: str


class GenreGateway:
    def __init__(self, db: DBTemplate) -> None:
        self.__db = db

    def list_all(self, conn: Optional[Connection] = None) -> List[GenreRecord]:
        query = """
            select * from genre
            order by genre asc;
        """
        rows = self.__db.query(statement=query, connection=conn)
        return map_results(
            rows, lambda row: GenreRecord(
                id=row["id"],
                genre=row["genre"]
            )
        )

    def get_by_id(self, id: int, conn: Optional[Connection] = None) -> Union[None, GenreRecord]:
        query = """
            select * from genre
            where id = :id
            limit 1;
        """
        rows = self.__db.query(statement=query, connection=conn, id=id)
        return map_result(
            rows,
            lambda row: GenreRecord(
                id=row["id"],
                genre=row["genre"]
            )
        )
