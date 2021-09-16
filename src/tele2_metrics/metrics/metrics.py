from tele2_metrics.metrics.dataframe_loader import LoadDataFrame
from tele2_metrics.utils.logs_maker import init_logger
from tele2_metrics.sql.templates.sql_get_number_of_rows import count_duplicates
from tele2_metrics.utils.send_email import notifiable
from tele2_metrics.metrics.error_messages import *
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

    @notifiable
    def compare_new_df_with_retro(self, notify: int = 0,
                                  conn_lib: str = 'teradatasql',
                                  condition: str = 'actual_df',
                                  sql_expr: str = None):
        actual_df = LoadDataFrame(settings.METRICS_STAGE_DB, conn_lib=conn_lib)\
            .get_df_with_rows_count(condition, settings.METRICS_STAGE_TABLE, sql_expr)
        retro_df = LoadDataFrame(settings.METRICS_FINAL_DB, conn_lib=conn_lib)\
            .get_df_with_rows_count(settings.METRICS_RETRO_TYPE, settings.METRICS_FINAL_TABLE)
        bool = self.compare_two_numbers(self.get_statistics_metric(retro_df, 'cnt', 'mean'),
                                        self.get_statistics_metric(actual_df, 'cnt', 'mean'),
                                        settings.METRICS_THRESHOLD)
        if bool is False:
            logger.error(error_text_compare_with_retro)
            return 'Error! Stop', notify, error_text_compare_with_retro

    @notifiable
    def check_if_data_in_table(self, notify: int = 0, conn_lib: str = 'teradatasql'):
        ldf = LoadDataFrame(settings.METRICS_FINAL_DB, conn_lib=conn_lib)
        df = ldf.get_df_with_rows_count('actual_df', settings.METRICS_FINAL_TABLE)
        text = error_text_no_data
        if df.empty:
            logger.error(text)
            return 'Error! Stop', notify, text

    @notifiable
    def check_df_for_duplicates(self, notify: int = 0, conn_lib: str = 'teradatasql'):
        ldf = LoadDataFrame(settings.METRICS_STAGE_DB, conn_lib=conn_lib)
        df = ldf.load_data(count_duplicates(settings.METRICS_STAGE_TABLE, settings.METRICS_COLUMN))
        if df['cnt'][0] != 0:
            logger.error(error_text_duplicates)
            return 'Error! Stop', notify, error_text_duplicates
