from tele2_metrics.sql.templates import sql_get_number_of_rows as sql
import unittest
from dynaconf import settings


class TestMetrics(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_count_rows_for_report_date(self):
        settings.METRICS_MODEL_ID = 42
        settings.METRICS_REPORT_DATE = '1977-05-25'
        temp = sql.count_rows_for_report_date(table_name='kaer.morhen')
        result = """
    SELECT Count(*) as cnt
    FROM kaer.morhen
    WHERE model_id = 42 AND report_date = DATE'1977-05-25'
    GROUP BY report_date, model_id
    """
        self.assertEqual(temp, result)

    def test_count_rows_for_retro(self):
        settings.METRICS_RETRO_DATE = '1977-05-25'
        settings.METRICS_REPORT_DATE = '2005-05-19'
        settings.METRICS_MODEL_ID = 42
        temp = sql.count_rows_for_retro(table_name='kaer.morhen', condition='retro_df')
        result = """
    SELECT Count(*) as cnt
    FROM kaer.morhen
    WHERE model_id = 42 AND report_date = DATE'1977-05-25'
    GROUP BY report_date, model_id
    """
        self.assertEqual(temp, result)
        temp = sql.count_rows_for_retro(table_name='kaer.morhen', condition='retro_df_many_dates')
        result = """
    SELECT Count(*) as cnt
    FROM kaer.morhen
    WHERE model_id = 42 AND report_date >= DATE'1977-05-25' AND report_date < DATE'2005-05-19'
    GROUP BY report_date, model_id
    """
        self.assertEqual(temp, result)

    def test_count_rows_with_expr(self):
        temp = sql.count_rows_with_expr('kaer.morhen', '')
        result = """
    SELECT Count(*) AS cnt
    FROM kaer.morhen
    
    """
        self.assertEqual(temp, result)
        temp = sql.count_rows_with_expr('kaer.morhen', "WHERE name = 'Geralt of Rivia'")
        result = """
    SELECT Count(*) AS cnt
    FROM kaer.morhen
    WHERE name = 'Geralt of Rivia'
    """
        self.assertEqual(temp, result)

    def test_count_duplicates(self):
        temp = sql.count_duplicates('kaer.morhen', 'witchers')
        result = f"""
    SELECT Count(*) AS cnt FROM (
        SELECT Count(*) AS cnt
        FROM kaer.morhen
        GROUP BY witchers
        HAVING Cnt > 1 
    ) t
    """
        self.assertEqual(temp, result)


if __name__ == '__main__':
    unittest.main()
