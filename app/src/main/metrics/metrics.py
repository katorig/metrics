from metrics.dataframe_loader import LoadDataFrame
from utils.logs_maker import init_logger
from sql.templates.sql_get_number_of_rows import count_duplicates
from utils.send_email import notification
from metrics.error_messages import *
from dynaconf import settings

logger = init_logger(__name__)


class Metrics:
    @staticmethod
    def get_statistics_metric(df, col, statistics_metric):
        value = getattr(df[col], statistics_metric)()
        logger.info(value)
        return value

    @staticmethod
    def compare_two_numbers(old_value, new_value, threshold: int) -> bool:
        share = round((new_value - old_value) / old_value * 100, 3)
        if share >= threshold or share <= -threshold:
            logger.error(f"Big difference between two values: {share}%! Check sources.")
            return False
        logger.info(f"Difference between two values is {share} %")
        return True

    @notification
    def compare_new_df_with_retro(self, notify: int = 0):
        actual_df = LoadDataFrame(settings.M_STAGE_DB)\
            .get_df_with_rows_count('actual_df', settings.M_STAGE_TABLE)
        retro_df = LoadDataFrame(settings.M_FINAL_DB)\
            .get_df_with_rows_count(settings.M_RETRO_TYPE, settings.M_FINAL_TABLE)
        bool = self.compare_two_numbers(self.get_statistics_metric(retro_df, 'cnt', 'mean'),
                                        self.get_statistics_metric(actual_df, 'cnt', 'mean'),
                                        settings.M_THRESHOLD)
        if bool is False:
            logger.error(error_text_compare_with_retro)
            return 'Error! Stop', notify, error_text_compare_with_retro

    @notification
    def check_if_data_in_table(self, notify: int = 0):
        ldf = LoadDataFrame(settings.M_FINAL_DB)
        df = ldf.get_df_with_rows_count('actual_df', settings.M_FINAL_TABLE)
        text = error_text_no_data
        if df.empty:
            logger.error(text)
            return 'Error! Stop', notify, text

    @notification
    def check_df_for_duplicates(self, notify: int = 0):
        ldf = LoadDataFrame(settings.M_STAGE_DB)
        df = ldf.load_data(count_duplicates(settings.M_STAGE_TABLE, settings.M_COLUMN))
        if df['cnt'][0] != 0:
            logger.error(error_text_duplicates)
            return 'Error! Stop', notify, error_text_duplicates
