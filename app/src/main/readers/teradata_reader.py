from pandas import DataFrame
from turbodbc import connect, make_options, Megabytes
import os
from dynaconf import settings

TERADATA_USER = os.environ.get('TERADATA_USER')
TERADATA_PASSWORD = os.environ.get('TERADATA_PASSWORD')


class TeradataService:

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self._con = None

    def execute_query(self, operation):
        with self._con.cursor() as cursor:
            cursor.execute(operation)
            table = DataFrame(cursor.fetchallnumpy())
            table.columns = table.columns.str.lower()
            return table

    def execute_ddl(self, operation):
        with self._con.cursor() as cursor:
            cursor.execute(operation)

    @staticmethod
    def _create_string():
        return f"""DBCName={settings.TERADATA_HOST};CharacterSet=UTF8;
Driver={settings.TERADATA_DRIVER};UID={TERADATA_USER};PWD={TERADATA_PASSWORD}"""

    def _connect(self):
        return connect(connection_string=self._create_string(),
                       turbodbc_options=make_options(read_buffer_size=Megabytes(42),
                                                     use_async_io=True,
                                                     prefer_unicode=True), **self._kwargs)

    def __enter__(self):
        self._con = self._connect()
        return self

    def __exit__(self, *args, **kwargs):
        self._con.close()
        self._con = None
        return False
