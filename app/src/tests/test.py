from main.metrics.metrics import Metrics
import unittest
import pandas as pd
from dynaconf import settings

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
    #     self.assertIsNone(mtr.compare_two_numbers(14522912, 14530000, 20))
    #     self.assertEqual(mtr.compare_two_numbers(14522912, 30000000, 20), False)

    def test_compare_new_df_with_retro(self):
        mtr = Metrics()
        k = mtr.compare_new_df_with_retro(135, 'developers.eg_msg_traf_1', 'hadoop', 'prd2_dds_v.scoring', 'teradata',
                                          15, '2021-03-04', '2021-06-04')
        self.assertEqual('Error! Send notification', k)


if __name__ == '__main__':
    unittest.main()
