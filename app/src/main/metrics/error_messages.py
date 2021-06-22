from dynaconf import settings as envs

error_text_duplicates = f"""В результатах скоринга модели (таблица {envs.M_STAGE_TABLE}) содержатся дубли. 
Скоринг остановлен. Проверьте модель"""
error_text_compare_with_retro = """Обнаружено падение/увеличение объема результатов скоринга модели. 
Скоринг остановлен. Проверьте модель"""
error_text_no_data = f"""Модель отработала, но результаты не были доставлены в {envs.M_FINAL_TABLE}.
Проверьте модель"""


