from tele2_metrics.connectors.hadoop_connector import HiveAdapter
import unittest


class TestConnectors(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_connect(self):
        cl = HiveAdapter()
        self.assertIsNone(cl._connect().close())


if __name__ == '__main__':
    unittest.main()
