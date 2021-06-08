import argparse

from metrics.dataframe_loader import LoadDataFrame
from metrics.metrics import Metrics
import time
from dynaconf import settings
import datetime as dt

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
    settings.MODEL_ID = args.model_id
    settings.REPORT_DATE = args.report_date
    return args.model_id, args.report_date


def check_if_results_appear_in_all_teradata_prod_tables(db, model_id, report_date):
    mtr = Metrics('ekaterina.gruzdova@tele2.ru', 'Check scoring tables', 'error')
    mtr.check_if_data_in_table(db, model_id, 'prd_dm.scoring', report_date=report_date)
    time.sleep(60 * 60 * 2)
    mtr.check_if_data_in_table(db, model_id, 'prd2_dds_v.scoring', report_date=report_date)
    time.sleep(60 * 60 * 24)
    mtr.check_if_data_in_table(db, model_id, 'prd2_bds_v.subs_score_current', report_date=report_date)


if __name__ == '__main__':
    model_id = 135
    report_date = '2021-06-04'
    retro_date = str((dt.datetime.strptime(report_date, '%Y-%m-%d') - dt.timedelta(days=90)).date())
    print(retro_date)

    # dpl = Metrics('ekaterina.gruzdova@tele2.ru', 'Data contains duplicates', 'error')
    # dpl.check_df_for_duplicates('hadoop', 'developers.eg_msg_traf_1', 'subs_id')
    rtr = Metrics('ekaterina.gruzdova@tele2.ru', 'Big difference in dataframes', 'error')
    rtr.compare_new_df_with_retro(model_id, 'developers.eg_msg_traf_1', 'hadoop', 'prd2_dds_v.scoring', 'teradata',
                                  15, retro_date, report_date)
    # check_if_results_appear_in_all_teradata_prod_tables('teradata', model_id, report_date)
