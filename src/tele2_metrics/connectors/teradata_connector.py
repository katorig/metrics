from pandas import DataFrame
import teradatasql
import os
from dynaconf import settings


class TeradataAdapter:

    def __init__(self, conn_lib='teradatasql'):
        self.conn_lib = conn_lib
        self._con = None

    def execute_query(self, operation):  # pragma: no cover
        with self._con.cursor() as cursor:
            cursor.execute(operation)
            if self.conn_lib == 'turbodbc':
                table = DataFrame(cursor.fetchallnumpy())
                table.columns = table.columns.str.lower()
            elif self.conn_lib == 'teradatasql':
                table = DataFrame(cursor.fetchall(),
                                  columns=[x[0] for x in cursor.description])
            return table

    def _connect(self):
        if os.environ.get('TERADATA_USER') is None or os.environ.get('TERADATA_PASSWORD') is None:
            TERADATA_USER = settings.TERADATA_USER
            TERADATA_PASSWORD = settings.TERADATA_PASSWORD
        else:
            TERADATA_USER = os.environ.get('TERADATA_USER')
            TERADATA_PASSWORD = os.environ.get('TERADATA_PASSWORD')
        if self.conn_lib == 'turbodbc':
            import turbodbc as tbd
            connection_string = f"""DSN=Teradata;DBCName={settings.TERADATA_HOST};
UID={TERADATA_USER};PWD={TERADATA_PASSWORD};CharacterSet=UTF8"""
            return tbd.connect(connection_string=connection_string,
                               turbodbc_options=tbd.make_options(prefer_unicode=True, autocommit=True))
        elif self.conn_lib == 'teradatasql':
            kwargs = {'host': settings.TERADATA_HOST, 'user': TERADATA_USER, 'password': TERADATA_PASSWORD}
            if settings.exists('LOGIN_TYPE') and settings.LOGIN_TYPE == 'domen':
                kwargs['logmech'] = 'LDAP'
                return teradatasql.connect(None, **kwargs)
            else:
                return teradatasql.connect(None, **kwargs)

    def __enter__(self):  # pragma: no cover
        self._con = self._connect()
        return self

    def __exit__(self, *args, **kwargs):  # pragma: no cover
        self._con.close()
        self._con = None
        return False
