from metrics.dataframe_loader import LoadDataFrame
from utils.logs_maker import init_logger
from sql.templates.sql_get_number_of_rows import count_duplicates
from utils.send_email import notification

logger = init_logger(__name__)


class Metrics:
    def __init__(self, send_to=None, subject=None, message=None):
        self.send_to = send_to
        self.subject = subject
        self.message = message
        self.notify = 'Error! Send notification'

    @staticmethod
    def get_statistics_metric(df, col, statistics_metric):
        value = getattr(df[col], statistics_metric)()
        logger.info(value)
        return value

    def compare_two_numbers(self, old_value, new_value, threshold: int):
        share = round((new_value - old_value) / old_value * 100, 3)

        @notification(self.send_to, self.subject, self.message)
        def check_threshold():
            if share >= threshold or share <= -threshold:
                logger.error(f"Big difference between two values: {share}%! Check sources.")
                return self.notify
            logger.info(f"Difference between two values is {share} %")

        check_threshold()

    def check_if_data_in_table(self, db_1, model_id, table_name, retro_date: str = None, report_date: str = None):
        ldf = LoadDataFrame(db_1)
        df = ldf.get_df_with_rows_count(table_name, model_id, retro_date, report_date)

        @notification(self.send_to, self.subject, self.message)
        def check():
            if df.empty:
                logger.error(f"No data found in {table_name}!")
                return self.notify

        check()

    def compare_new_df_with_retro(self, model_id,
                                  table_name, db_1, scoring_table_name, db_2,
                                  threshold, retro_date,
                                  report_date):
        actual_df = LoadDataFrame(db_1).get_df_with_rows_count(table_name, model_id, report_date)
        retro_df = LoadDataFrame(db_2).get_df_with_rows_count(scoring_table_name, model_id, retro_date, report_date)
        self.compare_two_numbers(self.get_statistics_metric(retro_df, 'cnt', 'mean'),
                                 self.get_statistics_metric(actual_df, 'cnt', 'mean'),
                                 threshold)

    def check_df_for_duplicates(self, db, table_name: str, col_name: str):
        ldf = LoadDataFrame(db)
        df = ldf.load_data(count_duplicates(table_name, col_name))

        @notification(self.send_to, self.subject, self.message)
        def check():
            if df.empty is False:
                logger.error(f"Results of scoring contain duplicates in {table_name}. Check scoring process.")
                return self.notify

        check()
