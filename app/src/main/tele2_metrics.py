#!/usr/bin/env python3

from metrics.metrics import Metrics
from argparse import ArgumentParser
from dynaconf import settings
from utils.logs_maker import init_logger
import sys

logger = init_logger(__name__)


def define_main_args_parser(choices_list: list) -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("method",
                        nargs="?",
                        help="""Type name of method you want to run.
Possible methods: check_df_for_duplicates, compare_new_df_with_retro, check_if_data_in_table.
Default method: no_function.
If you want to send notification add --emails parameter.""",
                        choices=choices_list,
                        default='no_function',
                        )
    parser.add_argument('--emails', metavar='emails', type=str, default=None,
                        help="type emails comma separated, i.e. 'e@a.ru, u@a.ru'")
    return parser


def foo(*args):
    logger.error("""Error! Choose method to run! 
Possible methods: check_df_for_duplicates, compare_new_df_with_retro, check_if_data_in_table""")
    sys.exit(1)


def call_check_df_for_duplicates():
    mtr.check_df_for_duplicates(send_to=args.emails,
                                subject=f'{email_subj} В результатах содержатся дубли',
                                text=f"""В результатах скоринга модели содержатся дубли. 
    Скоринг остановлен. Проверьте модель""")


def call_compare_new_df_with_retro():
    mtr.compare_new_df_with_retro(send_to=args.emails,
                                  subject=f'{email_subj} Некорректный объем значений',
                                  text=f"""Обнаружено падение/увеличение объема результатов скоринга модели. 
    Скоринг остановлен. Проверьте модель""")


def call_check_if_data_in_table():
    mtr.check_if_data_in_table(send_to=args.emails, subject=f'{email_subj} Нет результатов в {settings.M_FINAL_TABLE}',
                               text=f"""Модель отработала, но результаты не были доставлены в {settings.M_FINAL_TABLE}.
    Проверьте модель""")


if __name__ == '__main__':
    mtr = Metrics()
    email_subj = f"Ошибка модели {settings.M_MODEL_ID}."
    dictionary = {"no_function": foo,
                  "check_df_for_duplicates": call_check_df_for_duplicates,
                  "compare_new_df_with_retro": call_compare_new_df_with_retro,
                  "check_if_data_in_table": call_check_if_data_in_table}
    choices_list = list(dictionary.keys())
    parser = define_main_args_parser(choices_list)

    args, sub_args = parser.parse_known_args()

    dictionary.get(args.method)()
