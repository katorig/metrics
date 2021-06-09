from metrics.metrics import Metrics
import time
from dynaconf import settings
import datetime as dt


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

    dpl = Metrics('ekaterina.gruzdova@tele2.ru', 'Data contains duplicates', 'error')
    dpl.check_df_for_duplicates('hadoop', 'developers.eg_msg_traf_1', 'subs_id')
    rtr = Metrics('ekaterina.gruzdova@tele2.ru', 'Big difference in dataframes', 'error')
    rtr.compare_new_df_with_retro(model_id, 'developers.eg_msg_traf_1', 'hadoop', 'prd2_dds_v.scoring', 'teradata',
                                  15, retro_date, report_date)
    # check_if_results_appear_in_all_teradata_prod_tables('teradata', model_id, report_date)
