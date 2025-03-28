import unittest

from rmatzke.components.other import other_gateway


class OtherGatewayTestCase(unittest.TestCase):

    def test_get_other(self):
        self.assertEqual(other_gateway.get_other(1), "other_1")
        self.assertEqual(other_gateway.get_other(2), "other_2")
