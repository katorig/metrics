from metrics.metrics import Metrics
from argparse import ArgumentParser
from dynaconf import settings


if __name__ == '__main__':
    mtr = Metrics()
    email_subj = f"Ошибка модели {settings.M_MODEL_ID}."

    parser = ArgumentParser()
    parser.add_argument("method",
                        nargs="?",
                        help="""Type name of method you want to run.
    Possible methods: check_df_for_duplicates, compare_new_df_with_retro, check_if_data_in_table
    Default method: check_if_data_in_table""",
                        choices=['check_df_for_duplicates', 'compare_new_df_with_retro', 'check_if_data_in_table'],
                        default='check_if_data_in_table',
                        )
    parser.add_argument('--emails', metavar='emails', type=str, default=None,
                        help="type emails comma separated, i.e. 'e@a.ru, u@a.ru'")
    args, sub_args = parser.parse_known_args()



    if args.method == "check_df_for_duplicates":
        print('1')
        mtr.check_df_for_duplicates(send_to=args.emails,
                                    subject=f'{email_subj} В результатах содержатся дубли',
                                    text=f"""В результатах скоринга модели содержатся дубли. 
Скоринг остановлен. Проверьте модель""")

    elif args.method == "compare_new_df_with_retro":
        parser = ArgumentParser()
        parser.add_argument('--retro_df', metavar='retro_df', type=str,
                            help='choose which dataframe you need: retro_df_with_delta or retro_df')
        sub_args = parser.parse_args(sub_args)
        mtr.compare_new_df_with_retro(sub_args.retro_df, send_to=args.emails,
                                      subject=f'{email_subj} Некорректный объем значений',
                                      text=f"""Обнаружено падение/увеличение объема результатов скоринга модели. 
Скоринг остановлен. Проверьте модель""")

    elif args.method == "check_if_data_in_table":
        mtr.check_if_data_in_table(send_to=args.emails, subject=f'{email_subj} Нет результатов в {settings.M_FINAL_TABLE}',
                                   text=f"""Модель отработала, но результаты не были доставлены в {settings.M_FINAL_TABLE}.
Проверьте модель""")

