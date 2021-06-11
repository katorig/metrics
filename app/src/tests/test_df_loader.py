from main.metrics.dataframe_loader import LoadDataFrame
import unittest
import pandas as pd


class TestLoadDataFrame(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_load_data_teradata(self):
        l = LoadDataFrame('teradata')
        df_h = l.load_data("SELECT TOP 2 * FROM prd2_dds_v.scoring")
        self.assertEqual(df_h.shape[0], 2)

    def test_load_data_hadoop(self):
        l = LoadDataFrame('hadoop')
        df_h = l.load_data("SELECT * FROM geo.track limit 2")
        self.assertEqual(df_h.shape[0], 2)

    def test_get_df_with_rows_count_expr(self):
        l = LoadDataFrame('hadoop')
        df = l.get_df_with_rows_count('geo.track', expr=f'WHERE start_dttm_year = 2021 and start_dttm_month = 6 and start_dttm_day = 4')
        self.assertEqual(df['cnt'][0], 645579769)

    def test_get_df_with_rows_count_dates(self):
        l = LoadDataFrame('teradata')
        t = 'prd2_dds_v.scoring'
        df_1 = l.get_df_with_rows_count(t, 394, retro_date='2021-02-17', report_date='2021-05-17')
        self.assertGreater(len(df_1['cnt']), 1)
        df_2 = l.get_df_with_rows_count(t, 394, retro_date='2021-02-17')
        self.assertEqual(len(df_2['cnt']), 1)
        df_3 = l.get_df_with_rows_count(t, 394, report_date='2021-05-17')
        self.assertEqual(len(df_3['cnt']), 1)


if __name__ == '__main__':
    unittest.main()
