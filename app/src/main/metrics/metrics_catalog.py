from metrics.metrics import Metrics as mtr
import sys
from utils.logs_maker import init_logger
from dynaconf import settings as envs

logger = init_logger(__name__)


def foo():
    logger.error(f"Error! Choose method to run! Possible methods: {', '.join(methods_dict[1:])}")
    sys.exit(1)


error_text_duplicates = f"""В результатах скоринга модели (таблица {envs.M_STAGE_TABLE}) содержатся дубли. 
Скоринг остановлен. Проверьте модель"""
error_text_compare_with_retro = """Обнаружено падение/увеличение объема результатов скоринга модели. 
Скоринг остановлен. Проверьте модель"""
error_text_no_data = f"""Модель отработала, но результаты не были доставлены в {envs.M_FINAL_TABLE}.
Проверьте модель"""

methods_dict = {"no_function": foo,
                "check_df_for_duplicates": mtr.check_df_for_duplicates,
                "compare_new_df_with_retro": mtr.compare_new_df_with_retro,
                "check_if_data_in_table": mtr.check_if_data_in_table}




