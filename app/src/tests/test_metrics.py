from main.metrics.metrics import Metrics
import unittest
import pandas as pd

send_to = 'ekaterina.gruzdova@tele2.ru'
text = 'error'


class TestMetrics(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_get_statistics_metric(self):
        mtr = Metrics()
        df = pd.read_csv('df_test.csv', sep='\t', encoding='utf-8')
        value = round(mtr.get_statistics_metric(df, 'cnt', 'mean'), 3)
        self.assertEqual(value, 14522912.364)

    def test_compare_two_numbers(self):
        mtr = Metrics()
        self.assertEqual(mtr.compare_two_numbers(14522912, 14530000, 20), True)
        self.assertEqual(mtr.compare_two_numbers(14522912, 30000000, 20), False)

    def test_compare_new_df_with_retro(self):
        mtr = Metrics()
        k = mtr.compare_new_df_with_retro(135, 'developers.eg_msg_traf_1', 'hadoop', 'prd2_dds_v.scoring', 'teradata',
                                          15, '2021-03-04', '2021-06-04')
        self.assertEqual('Error! Send notification', k)
        mtr.compare_new_df_with_retro(135, 'developers.eg_msg_traf_1', 'hadoop', 'prd2_dds_v.scoring', 'teradata',
                                      15, '2021-03-04', '2021-06-04', send_to=send_to,
                                      subject='Big difference in dataframes', text=text)
        b = mtr.compare_new_df_with_retro(135, 'developers.eg_msg_traf_1', 'hadoop', 'prd2_dds_v.scoring', 'teradata',
                                          1000, '2021-03-04', '2021-06-04')
        self.assertIsNone(b)

    def test_check_if_data_in_table(self):
        mtr = Metrics()
        k = mtr.check_if_data_in_table('teradata', 326, 'prd2_dds_v.scoring', '2300-03-17')
        self.assertEqual('Error! Send notification', k)
        mtr.check_if_data_in_table('teradata', 326, 'prd2_dds_v.scoring', '2300-03-17', send_to=send_to,
                                   subject='No data in table {}!'.format('prd2_dds_v.scoring'), text=text)
        b = mtr.check_if_data_in_table('teradata', 326, 'prd2_dds_v.scoring', '2021-03-17')
        self.assertIsNone(b)

    def test_check_df_for_duplicates(self):
        mtr = Metrics()
        k = mtr.check_df_for_duplicates('hadoop', 'developers.eg_msg_traf_1', 'subs_id')
        self.assertEqual('Error! Send notification', k)
        mtr.check_df_for_duplicates('hadoop', 'developers.eg_msg_traf_1', 'subs_id', send_to=send_to,
                                    subject='Data contains duplicates in {}!'.format('developers.eg_msg_traf_1'),
                                    text=text)
        b = mtr.check_df_for_duplicates('teradata', 'PRD2_TMD_V.BDS_LOAD_STATUS', 'table_name')
        self.assertIsNone(b)


if __name__ == '__main__':
    unittest.main()
