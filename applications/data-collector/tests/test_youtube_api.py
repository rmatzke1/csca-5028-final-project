import sys
sys.path.append('./src')

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

with patch.dict('os.environ', {
    'YOUTUBE_API_KEY': 'fake_key',
    'DATABASE_URI': 'fake_uri',
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'COLLECTOR_DEFAULT_PUBLISHED_BEFORE': '2024-01-01 00:00:00',
    'COLLECTOR_RUN_DELTA': '1',
    'REDIS_HOST': 'localhost',
    'REDIS_PORT': '6379',
    'REDIS_SET_KEY': 'test_key'
}):
    import youtube_api


class YoutubeAPITestCase(unittest.TestCase):

    @patch('requests.get', autospec=True)
    def test_get_channel_id_by_handle(self, mock_requests_get):
        mock_requests_get.return_value.json.return_value = {
            "items": [{ "id": "fake_id" }]
        }
        result = youtube_api.get_channel_id_by_handle("fake_handle")
        self.assertEqual(result, "fake_id")

        mock_requests_get.assert_called_once_with(
            url="https://youtube.googleapis.com/youtube/v3/channels",
            params={
                "part": "snippet",
                "forHandle": "fake_handle",
                "maxResults": 1,
                "key": "fake_key",
            }
        )

    @patch('requests.get', autospec=True)
    def test_get_video_data(self, mock_requests_get):
        mock_requests_get.return_value.json.return_value = {
            "items": [{ "id": "fake_id" }]
        }
        published_before = datetime.strptime("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        published_after = published_before - timedelta(days=1)
        youtube_api.get_video_data(
            channel_id="fake_handle",
            published_before=published_before,
            published_after=published_after
        )
        mock_requests_get.assert_called_once_with(
            url="https://youtube.googleapis.com/youtube/v3/search",
            params={
                "part": "snippet",
                "channelId": "fake_handle",
                "maxResults": 25,
                "order": "date",
                "key": "fake_key",
                "published_before": published_before.isoformat() + "Z",
                "published_after": published_after.isoformat() + "Z",
            }
        )


if __name__ == "__main__":
    unittest.main()
