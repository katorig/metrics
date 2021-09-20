from tele2_metrics.connectors.teradata_connector import TeradataAdapter
import unittest
from dynaconf import settings


class TestConnectors(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_connect_turbodbc(self):
        cl = TeradataAdapter(conn_lib='turbodbc')
        self.assertIsNone(cl._connect().close())

    def test_connect_teradatasql(self):
        # service TERADATA_USER and TERADATA_PASSWORD were set in the environment
        cl = TeradataAdapter()
        self.assertIsNone(cl._connect().close())


class TestLdap(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def test_connect_ldap(self):
        # personal TERADATA_USER and TERADATA_PASSWORD were set in the environment
        settings.LOGIN_TYPE = 'domen'
        cl = TeradataAdapter()
        self.assertIsNone(cl._connect().close())
