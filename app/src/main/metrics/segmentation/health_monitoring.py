from sql.queries.scoring.templates import count_rows_in_prd_table
from readers.teradata_reader import read_teradata
import sys
import time
from utils.send_email import send_email_to_segmentation
from utils.logs_maker import init_logger


class SegmentationHealthMonitoring:
    def __init__(self, model_id: int, report_date: str):
        self.model_id = model_id
        self.report_date = report_date
        self.logger = init_logger()

    def set_monitoring_time_machine(self):
        self.check_data_in_prd_table('prd_dm.scoring')
        time.sleep(60 * 60 * 2)
        self.check_data_in_prd_table('prd2_dds_v.scoring')
        time.sleep(60 * 60 * 24)
        self.check_data_in_prd_table('prd2_bds_v.subs_score_current')

    def check_data_in_prd_table(self, prd_table_name: str):
        query = count_rows_in_prd_table.format(prd_table_name, self.model_id, self.report_date)
        df = read_teradata(query)
        if df.empty:
            self.logger.error(f"No data in {prd_table_name}!")
            send_email_to_segmentation(self.model_id, self.report_date)
            sys.exit(0)  # TODO: edit number of retries in project.yaml?
        else:
            self.logger.info(f"Data appeared in {prd_table_name}. Number of rows: {df['cnt'][0]}")
