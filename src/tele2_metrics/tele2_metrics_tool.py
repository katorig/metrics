#!/usr/bin/env python3

from argparse import ArgumentParser
from tele2_metrics.utils.logs_maker import init_logger
from dynaconf import settings
import sys

logger = init_logger(__name__)

settings.TERADATA_HOST = ''
settings.SEND_EMAIL_FROM = 'metrics@info.tele2.ru'
settings.HADOOP_HOST = ''
settings.HADOOP_PORT = 0
settings.KERBEROS_SERVICE_NAME = 'hive'
settings.SASL_AUTH = ''

def define_main_args_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("method",
                        nargs="?",
                        help=f"""
Type name of method you want to run.
Possible methods: "no_function", "check_df_for_duplicates", 
"compare_new_df_with_retro", "check_if_data_in_table".
Default method: no_function.
If you want to send notification add --notify parameter.""",
                        choices=["no_function", "check_df_for_duplicates",
"compare_new_df_with_retro", "check_if_data_in_table"],
                        default='no_function',
                        )
    parser.add_argument('--model_id', metavar='model_id', type=int, default=None,
                        help="ID of model, integer")
    parser.add_argument('--stage_db', metavar='stage_db', type=str, default=None,
                        help="teradata or hadoop")
    parser.add_argument('--stage_table', metavar='stage_table', type=str, default=None,
                        help="name of stage table in format schema.table")
    parser.add_argument('--final_db', metavar='final_db', type=str, default=None,
                        help="teradata or hadoop")
    parser.add_argument('--final_table', metavar='final_table', type=str, default=None,
                        help="name of final scoring table in format schema.table")
    parser.add_argument('--report_date', metavar='report_date', type=str, default=None,
                        help="report_date in format yyyy-mm-dd")
    parser.add_argument('--retro_date', metavar='retro_date', type=str, default=None,
                        help="retro date in format yyyy-mm-dd")
    parser.add_argument('--threshold', metavar='threshold', type=int, default=None,
                        help="""acceptable limit in percentage deviation 
                        between report_date scoring and retro_date scoring""")
    parser.add_argument('--column', metavar='column', type=str, default=None,
                        help="type columns which we have to group by to find duplicates. i.e. 'segment_id,subs_id'")
    parser.add_argument('--send_to', metavar='send_to', type=str, default=None,
                        help="emails for notification, i.e. 'y@a.ru,i@a.ru'")
    parser.add_argument('--retro_type', metavar='retro_type', type=str, default=None,
                        help="""
                        type 'retro_df' or 'retro_df_many_dates' depends on 
                        with which retro dataframe you want to compare actual dataframe""")
    parser.add_argument('--notify', metavar='notify', type=int, default=None,
                        help="1 is for notification by email or 0 is for no notification")
    return parser


def foo(*args):
    logger.error(f"""Error! Choose method to run! 
Possible methods: "no_function", "check_df_for_duplicates", 
"compare_new_df_with_retro", "check_if_data_in_table" """)
    sys.exit(1)


if __name__ == '__main__':
    parser = define_main_args_parser()
    args, sub_args = parser.parse_known_args()
    settings.METRICS_MODEL_ID = args.model_id
    settings.METRICS_STAGE_DB = args.stage_db
    settings.METRICS_STAGE_TABLE = args.stage_table
    settings.METRICS_FINAL_DB = args.final_db
    settings.METRICS_FINAL_TABLE = args.final_table
    settings.METRICS_REPORT_DATE = args.report_date
    settings.METRICS_RETRO_DATE = args.retro_date
    settings.METRICS_THRESHOLD = args.threshold
    settings.METRICS_COLUMN = args.column
    settings.METRICS_SEND_TO = args.send_to
    settings.METRICS_RETRO_TYPE = args.retro_type
    from tele2_metrics.metrics.metrics import Metrics
    mtr = Metrics()
    methods_dict = {"no_function": foo,
                    "check_df_for_duplicates": mtr.check_df_for_duplicates,
                    "compare_new_df_with_retro": mtr.compare_new_df_with_retro,
                    "check_if_data_in_table": mtr.check_if_data_in_table}
    methods_dict.get(args.method)(args.notify)
