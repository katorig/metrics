from tele2_metrics.metrics.metrics import Metrics
import unittest
import pandas
from dynaconf import settings

send_to = 'ekaterina.gruzdova@tele2.ru'
text = 'error'


class TestMetrics(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_get_statistics_metric(self):
        mtr = Metrics()
        df = pandas.read_csv('df_test.csv', sep='\t', encoding='utf-8')
        value = round(mtr.get_statistics_metric(df, 'cnt', 'mean'), 3)
        self.assertEqual(value, 14522912.364)

    def test_compare_two_numbers(self):
        mtr = Metrics()
        self.assertEqual(mtr.compare_two_numbers(14522912, 14530000, 20), True)
        self.assertEqual(mtr.compare_two_numbers(14522912, 30000000, 20), False)

    def test_compare_new_df_with_retro(self):
        mtr = Metrics()
        settings.METRICS_STAGE_DB = 'teradata'
        settings.METRICS_STAGE_TABLE = 'prd2_dds_v.scoring'
        settings.METRICS_MODEL_ID = 326
        settings.METRICS_REPORT_DATE = '2021-05-17'
        settings.METRICS_RETRO_DATE = '2021-03-17'
        self.assertIsNone(mtr.compare_new_df_with_retro())
        settings.METRICS_THRESHOLD = 0
        self.assertRaises(SystemExit, lambda: mtr.compare_new_df_with_retro())
        self.assertRaises(SystemExit, lambda: mtr.compare_new_df_with_retro(1))

    def test_check_if_data_in_table(self):
        mtr = Metrics()
        settings.METRICS_MODEL_ID = 326
        settings.METRICS_REPORT_DATE = '2300-03-17'
        self.assertRaises(SystemExit, lambda: mtr.check_if_data_in_table())
        self.assertRaises(SystemExit, lambda: mtr.check_if_data_in_table(1))
        settings.METRICS_REPORT_DATE = '2021-03-17'
        self.assertIsNone(mtr.check_if_data_in_table())

    def test_check_df_for_duplicates(self):
        mtr = Metrics()
        self.assertRaises(SystemExit, lambda: mtr.check_df_for_duplicates())
        self.assertRaises(SystemExit, lambda: mtr.check_df_for_duplicates(1))
        settings.METRICS_STAGE_DB = 'teradata'
        settings.METRICS_STAGE_TABLE = 'PRD2_TMD_V.BDS_LOAD_STATUS'
        settings.METRICS_COLUMN = 'table_name'
        b = mtr.check_df_for_duplicates()
        self.assertIsNone(b)


if __name__ == '__main__':
    unittest.main()
