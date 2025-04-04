import os
import sqlalchemy
import unittest
from datetime import datetime
from rmatzke.components.common.templates import DBTemplate
from rmatzke.components.collector.collector_run_gateway import CollectorRunGateway


class CollectorRunGatewayTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.engine = sqlalchemy.create_engine(os.getenv("TEST_DATABASE_URI"))
        self.db = DBTemplate(self.engine)
        self.prepare_data()
        self.collector_run_gateway = CollectorRunGateway(self.db)

    def prepare_data(self):
        query = """
            truncate table collector_run restart identity;
        """
        self.db.query(query)

    def test_insert(self):
        datetime_format = "%Y-%m-%d %H:%M:%S"
        self.collector_run_gateway.insert(
            run_start=datetime.strptime("2024-01-01 01:15:00", datetime_format),
            run_end=datetime.strptime("2024-01-01 01:15:30", datetime_format),
            param_published_before=datetime.strptime("2024-01-02 00:00:00", datetime_format),
            param_published_after=datetime.strptime("2024-01-01 00:00:00", datetime_format),
            video_count=3
        )

    def test_get_latest(self):
        datetime_format = "%Y-%m-%d %H:%M:%S"
        self.collector_run_gateway.insert(
            run_start=datetime.strptime("2025-01-01 01:15:00", datetime_format),
            run_end=datetime.strptime("2025-01-01 01:15:30", datetime_format),
            param_published_before=datetime.strptime("2025-01-02 00:00:00", datetime_format),
            param_published_after=datetime.strptime("2025-01-01 00:00:00", datetime_format),
            video_count=3
        )

        collector_run_record = self.collector_run_gateway.get_latest()
        self.assertEqual(
            collector_run_record.param_published_before,
            datetime.strptime("2025-01-02 00:00:00", datetime_format)
        )


if __name__ == "__main__":
    unittest.main()
