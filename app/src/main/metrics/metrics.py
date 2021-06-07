from metrics.dataframe_loader import LoadDataFrame
from utils.logs_maker import init_logger
from sql.templates.sql_get_number_of_rows import count_duplicates
import sys

logger = init_logger(__name__)


def get_statistics_metric(df, col, statistics_metric):
    value = getattr(df[col], statistics_metric)()
    logger.info(value)
    return value


def compare_two_numbers(old_value, new_value, threshold: int):
    share = round((new_value - old_value) / old_value * 100, 3)  # without abs() to see if deviation decreases
    if share >= threshold or share <= -threshold:
        logger.error(f"Big difference between two values: {share}%! Check sources.")
        sys.exit(1)
    logger.info(f"Difference between two values is {share} %")


def compare_new_df_with_retro(model_id,
                              table_name, db_1, scoring_table_name, db_2,
                              threshold, retro_date,
                              report_date):
    actual_ldf = LoadDataFrame(db_1, model_id, report_date)
    actual_df = actual_ldf.get_df_with_rows_count(table_name)
    retro_ldf = LoadDataFrame(db_2, model_id, report_date)
    retro_df = retro_ldf.get_df_with_rows_count(scoring_table_name, retro_date, report_date)
    compare_two_numbers(get_statistics_metric(retro_df, 'cnt', 'mean'),
                        get_statistics_metric(actual_df, 'cnt', 'mean'),
                        threshold)


def check_df_for_duplicates(db, model_id, report_date, table_name: str, col_name: str):
    ldf = LoadDataFrame(db, model_id, report_date)
    df = ldf.load_data(table_name, count_duplicates(table_name, col_name))
    if df.empty is False:
        logger.error(f"Table {table_name} contains duplicates. Check scoring process.")
