from pandas import DataFrame
import teradatasql
import os
from dynaconf import settings as envs

TERADATA_USER = os.environ.get('TERADATA_USER')
TERADATA_PASSWORD = os.environ.get('TERADATA_PASSWORD')


class TeradataService:

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
        return teradatasql.connect(None,
                                   host=envs.TERADATA_HOST,
                                   user=TERADATA_USER,
                                   password=TERADATA_PASSWORD)

    def __enter__(self):
        self._con = self._connect()
        return self

    def __exit__(self, *args, **kwargs):
        self._con.close()
        self._con = None
        return False
