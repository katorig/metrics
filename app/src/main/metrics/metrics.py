from metrics.dataframe_loader import LoadDataFrame
from utils.logs_maker import init_logger
from sql.templates.sql_get_number_of_rows import count_duplicates
from utils.send_email import notification
from dynaconf import settings as envs

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
    def compare_two_numbers(old_value, new_value, threshold: int) -> bool:
        share = round((new_value - old_value) / old_value * 100, 3)
        if share >= threshold or share <= -threshold:
            logger.error(f"Big difference between two values: {share}%! Check sources.")
            return False
        logger.info(f"Difference between two values is {share} %")
        return True

    @notification
    def compare_new_df_with_retro(self, which_retro: str, **kwargs):
        actual_df = LoadDataFrame(envs.M_STAGE_DB)\
            .get_df_with_rows_count('actual_df', envs.M_STAGE_TABLE)
        retro_df = LoadDataFrame(envs.M_FINAL_DB)\
            .get_df_with_rows_count(which_retro, envs.M_FINAL_TABLE)
        bool = self.compare_two_numbers(self.get_statistics_metric(retro_df, 'cnt', 'mean'),
                                        self.get_statistics_metric(actual_df, 'cnt', 'mean'),
                                        envs.M_THRESHOLD)
        if bool is False:
            return self.notify

    @notification
    def check_if_data_in_table(self, **kwargs):
        ldf = LoadDataFrame(envs.M_FINAL_DB)
        df = ldf.get_df_with_rows_count('actual_df', envs.M_FINAL_TABLE)
        if df.empty:
            logger.error(f"No data found in {envs.M_FINAL_TABLE}!")
            return self.notify

    @notification
    def check_df_for_duplicates(self, **kwargs):
        ldf = LoadDataFrame(envs.M_STAGE_DB)
        df = ldf.load_data(count_duplicates(envs.M_STAGE_TABLE, envs.M_COLUMN))
        if df['cnt'][0] != 0:
            logger.error(f"Results of scoring contain duplicates in {envs.M_STAGE_TABLE}. Check scoring process.")
            return self.notify
