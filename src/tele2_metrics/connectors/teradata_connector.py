from pandas import DataFrame
import teradatasql
import turbodbc as tbd
import os
from dynaconf import settings

TERADATA_USER = os.environ.get('TERADATA_USER')
TERADATA_PASSWORD = os.environ.get('TERADATA_PASSWORD')


class TeradataAdapter:

    def __init__(self, conn_lib='teradatasql'):
        self.conn_lib = conn_lib
        self._con = None

    def execute_query(self, operation):
        with self._con.cursor() as cursor:
            cursor.execute(operation)
            if self.conn_lib == 'turbodbc':
                table = DataFrame(cursor.fetchallnumpy())
                table.columns = table.columns.str.lower()
            elif self.conn_lib == 'teradatasql':
                table = DataFrame(cursor.fetchall(),
                                  columns=[x[0] for x in cursor.description])
            return table

    def execute_ddl(self, operation):
        with self._con.cursor() as cursor:
            cursor.execute(operation)

    def _connect(self):
        if self.conn_lib == 'turbodbc':
            params = {}
            # if settings.LOGIN_TYPE == 'domen':
            #     params['authentication'] = 'LDAP'
            connection_string = f"""DSN=Teradata;DBCName={settings.TERADATA_HOST};
UID={TERADATA_USER};PWD={TERADATA_PASSWORD};CharacterSet=UTF8"""
            return tbd.connect(connection_string=connection_string,
                               **params,
                               turbodbc_options=tbd.make_options(prefer_unicode=True, autocommit=True))
        elif self.conn_lib == 'teradatasql':
            return teradatasql.connect(None,
                                       host=settings.TERADATA_HOST,
                                       user=TERADATA_USER,
                                       password=TERADATA_PASSWORD)

    def __enter__(self):
        self._con = self._connect()
        return self

    def __exit__(self, *args, **kwargs):
        self._con.close()
        self._con = None
        return False
