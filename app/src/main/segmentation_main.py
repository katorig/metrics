import argparse

from metrics.dataframe_loader import LoadDataFrame
from metrics.metrics import Metrics
import time

subject = 'Недоступен скоринг модели {0} за {1}'
message = """
Добрый день, коллеги!

Отсутствуют результаты скоринга модели {0} за актуальную дату.
Требуется перезапуск модели и диагностика ситуации."""


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('model_id', metavar='model_id', type=int, help='Please type model_id')
    parser.add_argument('report_date', metavar='report_date', type=str,
                        help="Please type report_date in 'YYYY-MM-DD' format")
    args = parser.parse_args()
    return args.model_id, args.report_date


def check_if_results_appear_in_all_teradata_prod_tables(db, model_id, report_date):
    mon = LoadDataFrame(db, model_id, report_date)
    mon.get_df_with_rows_count('prd_dm.scoring')
    time.sleep(60 * 60 * 2)
    mon.get_df_with_rows_count('prd2_dds_v.scoring')
    time.sleep(60 * 60 * 24)
    mon.get_df_with_rows_count('prd2_bds_v.subs_score_current')


if __name__ == '__main__':
    model_id, report_date = parse_argument()
    retro_date = '2021-02-17'
    db = 'teradata'

    mtr = Metrics(db, model_id, report_date)
    mtr.compare_difference_in_rows_between_two_dfs('prd2_dds_v.scoring', 15, retro_date, report_date)
    check_if_results_appear_in_all_teradata_prod_tables(db, model_id, report_date)
