import unittest
from rmatzke.components.collector import collector_run_gateway


class CollectorRunGatewayTestCase(unittest.TestCase):

    def test_fake_test(self):
        self.assertEqual("a", "a")
        self.assertNotEqual("a", "b")
