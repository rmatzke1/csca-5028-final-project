from contextlib import _GeneratorContextManager
from typing import Any, Optional, TypeVar

import sqlalchemy
from sqlalchemy import Connection, CursorResult, Engine

T = TypeVar("T")


class DBTemplate:
    def __init__(self, engine: Engine) -> None:
        self.__engine = engine

    def begin(self) -> _GeneratorContextManager[Connection]:
        return self.__engine.begin()

    def query(
        self, statement: str, connection: Optional[Connection] = None, **kwargs: Any
    ) -> CursorResult[None]:
        if connection is None:
            with self.begin() as connection:
                return connection.execute(sqlalchemy.text(statement), kwargs)

        else:
            return connection.execute(sqlalchemy.text(statement), kwargs)
