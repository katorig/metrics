from sql.templates.sql_get_number_of_rows import count_rows_with_report_date
from sql.templates.sql_load_incr_dataframe import load_df
from readers.teradata_reader import read_teradata
import sys
from utils.logs_maker import init_logger

logger = init_logger()


class LoadDataFrame:
    def __init__(self,
                 model_id: int,
                 report_date: str):
        self.model_id = model_id
        self.report_date = report_date

    @staticmethod
    def load_data(table_name: str,
                  query: str):
        df = read_teradata(query)
        if df.empty:
            logger.error(f"Error! No data found in {table_name}!")
            sys.exit(1)
        logger.info(f"Table {table_name} contains necessary data.")
        return df

    def get_df_with_rows_count(self,
                               table_name: str,
                               retro_date: str = ''):
        return self.load_data(table_name, count_rows_with_report_date(table_name,
                                                                      self.model_id,
                                                                      self.report_date,
                                                                      retro_date))

    def get_whole_df_from_incr_partition(self,
                                         table_name: str):
        return self.load_data(table_name, load_df)
