from dataclasses import dataclass
from typing import List, Optional
from sqlalchemy import Connection
from rmatzke.components.common.mapper_funcs import map_results
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
            select * from genre;
        """
        result = self.__db.query(statement=query, connection=conn)
        return map_results(
            result, lambda row: GenreRecord(
                id=row["id"],
                genre=row["genre"]
            )
        )
