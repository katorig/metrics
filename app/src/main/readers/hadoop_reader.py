from pandas import DataFrame
from puretransport import transport_factory
from pyhive.hive import connect
from dynaconf import settings


class HiveService:

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self._con = None

    def execute_query(self, operation):
        with self._con.cursor() as cursor:
            cursor.execute(operation)
            table = DataFrame(cursor.fetchall(),
                              columns=[x[0] for x in cursor.description])
            return table

    def execute_ddl(self, operation):
        with self._con.cursor() as cursor:
            cursor.execute(operation)

    def _connect(self):
        transport = transport_factory(host=settings.HADOOP_HOST, port=settings.HADOOP_PORT,
                                      kerberos_service_name=settings.KERBEROS_SERVICE_NAME,
                                      sasl_auth=settings.SASL_AUTH, username=None, password=None,
                                      **self._kwargs)
        return connect(thrift_transport=transport)

    def __enter__(self):
        self._con = self._connect()
        return self

    def __exit__(self, *args, **kwargs):
        self._con.close()
        self._con = None
        return False
