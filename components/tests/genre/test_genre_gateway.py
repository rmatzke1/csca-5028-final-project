import os
import sqlalchemy
import unittest
from rmatzke.components.common.templates import DBTemplate
from rmatzke.components.genre.genre_gateway import GenreGateway


class GenreGatewayTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.engine = sqlalchemy.create_engine(os.getenv("TEST_DATABASE_URI"))
        self.db = DBTemplate(self.engine)
        self.prepare_data()
        self.genre_gateway = GenreGateway(self.db)

    def prepare_data(self):
        query = """
            truncate table genre restart identity;
            insert into genre (genre) values
                ('Genre1'),
                ('Genre2'),
                ('Genre3');
        """
        self.db.query(query)

    def test_list_all(self):
        genre_records = self.genre_gateway.list_all()
        self.assertEqual(len(genre_records), 3)

    def test_get_by_id(self):
        genre_record = self.genre_gateway.get_by_id(1)
        self.assertEqual(genre_record.genre, "Genre1")

    def test_get_by_id_not_found(self):
        genre_record = self.genre_gateway.get_by_id(0)
        self.assertIsNone(genre_record)


if __name__ == "__main__":
    unittest.main()
