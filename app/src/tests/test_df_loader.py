from main.metrics.dataframe_loader import LoadDataFrame
import unittest
import pandas as pd
from dynaconf import settings as envs


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
        df = l.get_df_with_rows_count('df_with_expr', 'geo.track', expr=f'WHERE start_dttm_year = 2021 and start_dttm_month = 6 and start_dttm_day = 4')
        self.assertEqual(df['cnt'][0], 645579769)

    def test_get_df_with_rows_count_dates(self):
        l = LoadDataFrame('teradata')
        t = 'prd2_dds_v.scoring'
        envs.M_REPORT_DATE = '2021-05-17'
        envs.M_RETRO_DATE = '2021-02-17'
        envs.M_MODEL_ID = 394
        df_1 = l.get_df_with_rows_count('retro_df_many_dates', t)
        self.assertGreater(len(df_1['cnt']), 1)
        df_2 = l.get_df_with_rows_count('retro_df', t)
        self.assertEqual(len(df_2['cnt']), 1)
        df_3 = l.get_df_with_rows_count('actual_df', t)
        self.assertEqual(len(df_3['cnt']), 1)


if __name__ == '__main__':
    unittest.main()
