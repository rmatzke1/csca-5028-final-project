import unittest

from rmatzke.videos import video_gateway


class VideoGatewayTestCase(unittest.TestCase):

    def test_get_video(self):
        self.assertEqual(video_gateway.get_video(1), "video_1")
        self.assertEqual(video_gateway.get_video(2), "video_2")
