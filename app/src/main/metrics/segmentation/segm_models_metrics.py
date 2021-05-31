from sql.queries.scoring.templates import retro_df_from_prd_table
from readers.teradata_reader import read_teradata
import sys
from utils.send_email import send_email_to_segmentation
from utils.logs_maker import init_logger
import pandas as pd


class SegmentationMetrics:
    def __init__(self, model_id: int, report_date: str):
        self.model_id = model_id
        self.report_date = report_date
        self.logger = init_logger()

    def check_number_of_rows(self, rows_cnt: int):
        query = retro_df_from_prd_table.format(self.model_id, self.report_date)
        retro_df = read_teradata(query)
        retro_mean = retro_df["cnt"].mean()
        share = round((rows_cnt - retro_mean) / retro_mean * 100)
        # if share >= 15 or share <= -15: