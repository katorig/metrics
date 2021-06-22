#!/usr/bin/env python3

from metrics.metrics import Metrics
from argparse import ArgumentParser
from utils.logs_maker import init_logger
import sys

logger = init_logger(__name__)


def define_main_args_parser(methods_list: list) -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("method",
                        nargs="?",
                        help=f"""
Don't forget to assign environment variables: 
DYNACONF_M_MODEL_ID (int)
DYNACONF_M_STAGE_DB (teradata or hadoop)
DYNACONF_M_STAGE_TABLE (name of stage table in format schema.table)
DYNACONF_M_FINAL_DB (teradata or hadoop)
DYNACONF_M_FINAL_TABLE (name of final scoring table in format schema.table)
DYNACONF_M_REPORT_DATE (report_date in format yyyy-mm-dd)
DYNACONF_M_RETRO_DATE (previous or retro date in format yyyy-mm-dd)
DYNACONF_M_THRESHOLD (acceptable limit in percentage deviation between report_date scoring and retro_date scoring)
DYNACONF_M_COLUMN (column for searching for duplicates)
DYNACONF_M_SEND_TO (emails for notification, i.e. 'y@a.ru, i@a.ru')
DYNACONF_M_RETRO_TYPE (type 'retro_df' or 'retro_df_many_dates' depends on with which retro dataframe you want to compare actual dataframe)
Type name of method you want to run.
Possible methods: {', '.join(methods_list[1:])}.
Default method: no_function.
If you want to send notification add --notify parameter.""",
                        choices=methods_list,
                        default='no_function',
                        )
    parser.add_argument('--notify', metavar='notify', type=int, default=None,
                        help="type 1 for notification by email or 0 for no notification")
    return parser


def foo(*args):
    logger.error(f"Error! Choose method to run! Possible methods: {', '.join(methods_list[1:])}")
    sys.exit(1)


if __name__ == '__main__':
    mtr = Metrics()
    methods_dict = {"no_function": foo,
                    "check_df_for_duplicates": mtr.check_df_for_duplicates,
                    "compare_new_df_with_retro": mtr.compare_new_df_with_retro,
                    "check_if_data_in_table": mtr.check_if_data_in_table}
    methods_list = list(methods_dict.keys())
    parser = define_main_args_parser(methods_list)
    args, sub_args = parser.parse_known_args()
    methods_dict.get(args.method)(args.notify)
