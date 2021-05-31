import pandas as pd
from turbodbc import connect, make_options, Megabytes
import os
from dynaconf import settings

TERADATA_USER = os.environ.get('TERADATA_USER')
TERADATA_PASSWORD = os.environ.get('TERADATA_PASSWORD')


def read_teradata(query) -> pd.DataFrame:
    """Execute SQL query in Teradata and save results to DataFrame
    Parameters:
        query (str): SQL query
    Returns:
        df (pandas.DataFrame): query results
    """
    con = connect(connection_string=f"""DBCName={settings.TERADATA_HOST};CharacterSet=UTF8;
Driver={settings.TERADATA_DRIVER};UID={TERADATA_USER};PWD={TERADATA_PASSWORD}""",
                  turbodbc_options=make_options(read_buffer_size=Megabytes(42),
                                                use_async_io=True,
                                                prefer_unicode=True)
                  )
    cursor = con.cursor()
    cursor.execute(query)
    df = pd.DataFrame(cursor.fetchallnumpy())
    df.columns = df.columns.str.lower()
    con.close()
    return df
