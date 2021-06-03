from metrics.dataframe_loader import LoadDataFrame
from utils.logs_maker import init_logger
import sys

logger = init_logger(__name__)


class Metrics(LoadDataFrame):
    def __init__(self, db, model_id: int, report_date: str):
        super().__init__(db, model_id, report_date)

    @staticmethod
    def get_statistics_metric(df, col, statistics_metric):
        value = getattr(df[col], statistics_metric)()
        return value

    @staticmethod
    def compare_two_numbers(old_value, new_value, threshold: int):
        share = round((new_value - old_value) / old_value * 100, 3)  # without abs() to see if deviation decreases
        if share >= threshold or share <= -threshold:
            logger.error("Big difference between two values! Check sources.")
            sys.exit(1)
        logger.info(f"Difference between two values is {share} %")

    def compare_difference_in_rows_between_two_dfs(self, table_name, threshold, retro_date,
                                                   report_date, col='cnt'):
        retro_df = self.get_df_with_rows_count(table_name, retro_date, report_date)
        actual_df = self.get_df_with_rows_count(table_name)
        self.compare_two_numbers(self.get_statistics_metric(retro_df, col, 'mean'),
                                 self.get_statistics_metric(actual_df, col, 'mean'),
                                 threshold)
