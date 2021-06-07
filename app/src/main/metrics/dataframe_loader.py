from sql.templates.sql_get_number_of_rows import count_rows_for_report_date, count_rows_for_retro
from sql.templates.sql_load_incr_dataframe import load_df
from readers.teradata_reader import TeradataService
from readers.hadoop_reader import HiveService
import sys
from utils.logs_maker import init_logger

logger = init_logger(__name__)


class LoadDataFrame:
    def __init__(self,
                 db,
                 model_id: int,
                 report_date: str):
        self.model_id = model_id
        self.report_date = report_date
        if db == 'hadoop':
            self.db = HiveService()
        elif db == 'teradata':
            self.db = TeradataService()

    def load_data(self, table_name: str, query: str):
        with self.db as service:
            df = service.execute_query(query)
        if df.empty:
            logger.error(f"Error! No data found in table {table_name}! Query: {query}")  # TODO: rewrite to throw exception
            sys.exit(1)
        logger.info(f"Table {table_name} contains necessary data.")
        return df

    def get_df_with_rows_count(self,
                               table_name: str,
                               retro_date: str = None,
                               report_date: str = None):
        if retro_date:
            return self.load_data(table_name,
                                  count_rows_for_retro(table_name, self.model_id, retro_date, report_date))
        elif retro_date is None:
            return self.load_data(table_name,
                                  count_rows_for_report_date(table_name, self.model_id, self.report_date))

    def get_whole_df_from_incr_partition(self,
                                         table_name: str):
        return self.load_data(table_name, load_df)
