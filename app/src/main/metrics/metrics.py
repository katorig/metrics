from metrics.dataframe_loader import LoadDataFrame
from utils.logs_maker import init_logger
from sql.templates.sql_get_number_of_rows import count_duplicates
from utils.send_email import notification

logger = init_logger(__name__)


class Metrics:
    def __init__(self):
        self.notify = 'Error! Send notification'

    @staticmethod
    def get_statistics_metric(df, col, statistics_metric):
        value = getattr(df[col], statistics_metric)()
        logger.info(value)
        return value

    @staticmethod
    def compare_two_numbers(old_value, new_value, threshold: int):
        share = round((new_value - old_value) / old_value * 100, 3)
        if share >= threshold or share <= -threshold:
            logger.error(f"Big difference between two values: {share}%! Check sources.")
            return False
        logger.info(f"Difference between two values is {share} %")

    @notification
    def compare_new_df_with_retro(self, model_id,
                                  table_name, db_1, scoring_table_name, db_2,
                                  threshold, retro_date,
                                  report_date, **kwargs):
        actual_df = LoadDataFrame(db_1).get_df_with_rows_count(table_name, model_id, report_date)
        retro_df = LoadDataFrame(db_2).get_df_with_rows_count(scoring_table_name, model_id, retro_date, report_date)
        bool = self.compare_two_numbers(self.get_statistics_metric(retro_df, 'cnt', 'mean'),
                                        self.get_statistics_metric(actual_df, 'cnt', 'mean'),
                                        threshold)
        if bool is False:
            return self.notify

    @notification
    def check_if_data_in_table(self, db_1, model_id, table_name,
                               retro_date: str = None, report_date: str = None, **kwargs):
        ldf = LoadDataFrame(db_1)
        df = ldf.get_df_with_rows_count(table_name, model_id, retro_date, report_date)
        if df.empty:
            logger.error(f"No data found in {table_name}!")
            return self.notify

    @notification
    def check_df_for_duplicates(self, db, table_name: str, col_name: str, **kwargs):
        ldf = LoadDataFrame(db)
        df = ldf.load_data(count_duplicates(table_name, col_name))
        if df.empty is False:
            logger.error(f"Results of scoring contain duplicates in {table_name}. Check scoring process.")
            return self.notify
