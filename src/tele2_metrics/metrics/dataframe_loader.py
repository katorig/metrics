from tele2_metrics.sql.templates.sql_get_number_of_rows import *
from tele2_metrics.connectors.teradata_connector import TeradataAdapter
from tele2_metrics.connectors.hadoop_connector import HiveAdapter
from tele2_metrics.utils.logs_maker import init_logger

logger = init_logger(__name__)


class LoadDataFrame:
    def __init__(self,
                 db, conn_lib='teradatasql'):
        if db == 'hadoop':
            self.db = HiveAdapter()
        elif db == 'teradata':
            self.db = TeradataAdapter(conn_lib)

    def load_data(self, query: str):
        with self.db as service:
            df = service.execute_query(query)
        return df

    def get_df_with_rows_count(self,
                               condition: str,
                               table_name: str,
                               expr: str = None):
        if condition == 'actual_df':
            return self.load_data(count_rows_for_report_date(table_name))
        elif condition == 'retro_df':
            return self.load_data(count_rows_for_retro(table_name, condition))
        elif condition == 'retro_df_many_dates':
            return self.load_data(count_rows_for_retro(table_name, condition))
        elif condition == 'df_with_expr':
            return self.load_data(count_rows_with_expr(table_name, expr))
