from metrics.metrics import Metrics
import time
import datetime as dt

send_to = 'ekaterina.gruzdova@tele2.ru'


def check_if_results_appear_in_all_teradata_prod_tables(db, model_id, report_date):
    mtr = Metrics()
    a = [db, model_id]
    subject = 'No data in table {0}!'
    text = 'error'
    mtr.check_if_data_in_table(*a, 'prd_dm.scoring', report_date=report_date,
                               send_to=send_to, subject=subject.format('prd_dm.scoring'), text=text)
    # time.sleep(60 * 60 * 2)
    # mtr.check_if_data_in_table(*a, 'prd2_dds_v.scoring', report_date=report_date,
    #                            send_to=send_to, subject=subject.format('prd2_dds_v.scoring'), text=text)
    # time.sleep(60 * 60 * 24)
    # mtr.check_if_data_in_table(*a, 'prd2_bds_v.subs_score_current', report_date=report_date,
    #                            send_to=send_to, subject=subject.format('prd2_bds_v.subs_score_current'), text=text)


if __name__ == '__main__':
    model_id = 135
    report_date = '2021-06-04'
    retro_date = str((dt.datetime.strptime(report_date, '%Y-%m-%d') - dt.timedelta(days=100)).date())

    mtr = Metrics()
    mtr.check_df_for_duplicates('hadoop', 'developers.eg_msg_traf_1', 'subs_id', send_to='ekaterina.gruzdova@tele2.ru',
                                subject='Data contains duplicates', text='error')
    mtr.compare_new_df_with_retro(model_id, 'developers.eg_msg_traf_1', 'hadoop', 'prd2_dds_v.scoring', 'teradata',
                                  15, retro_date, report_date, send_to='ekaterina.gruzdova@tele2.ru',
                                  subject='Big difference in dataframes', text='error')
    check_if_results_appear_in_all_teradata_prod_tables('teradata', model_id, report_date)
