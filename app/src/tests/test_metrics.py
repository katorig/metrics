from main.metrics.metrics import Metrics
import unittest
import pandas as pd
from dynaconf import settings

send_to = 'ekaterina.gruzdova@tele2.ru'
text = 'error'


class TestMetrics(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    # def test_get_statistics_metric(self):
    #     mtr = Metrics()
    #     df = pd.read_csv('df_test.csv', sep='\t', encoding='utf-8')
    #     value = round(mtr.get_statistics_metric(df, 'cnt', 'mean'), 3)
    #     self.assertEqual(value, 14522912.364)
    #
    # def test_compare_two_numbers(self):
    #     mtr = Metrics()
    #     self.assertEqual(mtr.compare_two_numbers(14522912, 14530000, 20), True)
    #     self.assertEqual(mtr.compare_two_numbers(14522912, 30000000, 20), False)
    #
    # def test_compare_new_df_with_retro(self):
    #     mtr = Metrics()
    #     settings.M_STAGE_DB = 'hadoop'
    #     settings.M_STAGE_TABLE = 'developers.eg_msg_traf_1'
    #     settings.M_MODEL_ID = 135
    #     settings.M_REPORT_DATE = '2021-06-04'
    #     k = mtr.compare_new_df_with_retro('retro_df_with_delta')
    #     self.assertEqual('Error! Send notification', k)
    #     mtr.compare_new_df_with_retro(send_to=send_to,
    #                                   subject='Big difference in dataframes', text=text)
    #     settings.M_THRESHOLD = 1000
    #     b = mtr.compare_new_df_with_retro('retro_df_with_delta')
    #     self.assertIsNone(b)
    #
    # def test_check_if_data_in_table(self):
    #     mtr = Metrics()
    #     settings.M_MODEL_ID = 326
    #     settings.M_REPORT_DATE = '2300-03-17'
    #     k = mtr.check_if_data_in_table()
    #     self.assertEqual('Error! Send notification', k)
    #     mtr.check_if_data_in_table(send_to=send_to,
    #                                subject='No data in table {}!'.format('prd2_dds_v.scoring'), text=text)
    #     settings.M_REPORT_DATE = '2021-03-17'
    #     b = mtr.check_if_data_in_table()
    #     self.assertIsNone(b)

    def test_check_df_for_duplicates(self):
        mtr = Metrics()
        k = mtr.check_df_for_duplicates()
        self.assertEqual('Error! Send notification', k)
        mtr.check_df_for_duplicates(send_to=send_to,
                                    subject='Data contains duplicates in {}!'.format('developers.eg_msg_traf_1'),
                                    text=text)
        settings.M_STAGE_DB = 'teradata'
        settings.M_STAGE_TABLE = 'PRD2_TMD_V.BDS_LOAD_STATUS'
        settings.M_COLUMN = 'table_name'
        b = mtr.check_df_for_duplicates()
        self.assertIsNone(b)


if __name__ == '__main__':
    unittest.main()
