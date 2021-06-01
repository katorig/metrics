from metrics.dataframe_loader import LoadDataFrame
import pandas as pd


class Metrics(LoadDataFrame):
    def __init__(self,
                 model_id: int,
                 report_date: str):
        super().__init__(model_id, report_date)

    @staticmethod
    def get_statistics_metric(df, col, statistics_metric):
        value = getattr(df[col], statistics_metric)()
        return value

    def get_stats_on_cnt_table(self, table_name, statistics_metric, retro_date=''):
        df = self.get_df_with_rows_count(table_name, retro_date)
        value = self.get_statistics_metric(df, 'cnt', statistics_metric)
        return value


