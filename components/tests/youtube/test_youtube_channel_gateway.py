import os
import sqlalchemy
import unittest
from rmatzke.components.common.templates import DBTemplate
from rmatzke.components.youtube.youtube_channel_gateway import YoutubeChannelGateway


class YoutubeChannelGatewayTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.engine = sqlalchemy.create_engine(os.getenv("TEST_DATABASE_URI"))
        self.db = DBTemplate(self.engine)
        self.prepare_data()
        self.youtube_channel_gateway = YoutubeChannelGateway(self.db)

    def prepare_data(self):
        query = """
            truncate table youtube_channel restart identity;
            insert into youtube_channel (youtube_handle) values
                ('YoutubeHandle1'),
                ('YoutubeHandle2'),
                ('YoutubeHandle3');
            insert into youtube_channel (youtube_handle, youtube_channel_id) values
                ('YoutubeHandle4', 'YoutubeChannelID4'),
                ('YoutubeHandle5', 'YoutubeChannelID5'),
                ('YoutubeHandle6', 'YoutubeChannelID6');                
        """
        self.db.query(query)

    def test_list_all(self):
        youtube_channel_records = self.youtube_channel_gateway.list_all()
        self.assertEqual(len(youtube_channel_records), 6)

    def test_list_with_channel_ids(self):
        youtube_channel_records = self.youtube_channel_gateway.list_with_channel_ids()
        self.assertNotEqual(len(youtube_channel_records), 0)
        for r in youtube_channel_records:
            self.assertTrue(r.youtube_channel_id)

    def test_list_without_channel_ids(self):
        youtube_channel_records = self.youtube_channel_gateway.list_without_channel_ids()
        self.assertNotEqual(len(youtube_channel_records), 0)
        for r in youtube_channel_records:
            self.assertFalse(r.youtube_channel_id)

    def test_set_channel_id(self):
        self.youtube_channel_gateway.set_channel_id(2, "YoutubeChannelID2")
        youtube_channel_records = self.youtube_channel_gateway.list_with_channel_ids()
        found = any(r.youtube_channel_id == "YoutubeChannelID2" for r in youtube_channel_records)
        self.assertEqual(found, True)


if __name__ == "__main__":
    unittest.main()
