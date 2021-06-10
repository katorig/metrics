from sql.templates.sql_get_number_of_rows import count_rows_for_report_date, count_rows_for_retro, count_rows_with_expr
from readers.teradata_reader import TeradataService
from readers.hadoop_reader import HiveService
from utils.logs_maker import init_logger

logger = init_logger(__name__)


class LoadDataFrame:
    def __init__(self,
                 db):
        if db == 'hadoop':
            self.db = HiveService()
        elif db == 'teradata':
            self.db = TeradataService()

    def load_data(self, query: str):
        with self.db as service:
            df = service.execute_query(query)
        return df

    def get_df_with_rows_count(self,
                               table_name: str,
                               model_id: int = None,
                               retro_date: str = None,
                               report_date: str = None,
                               expr: str = None):
        if model_id is None:
            return self.load_data(count_rows_with_expr(table_name, expr))
        else:
            if retro_date:
                return self.load_data(count_rows_for_retro(table_name, model_id, retro_date, report_date))
            elif retro_date is None:
                return self.load_data(count_rows_for_report_date(table_name, model_id, report_date))
