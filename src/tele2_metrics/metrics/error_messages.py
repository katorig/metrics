from dynaconf import settings

error_text_duplicates = f"""В результатах скоринга модели (таблица {settings.METRICS_STAGE_TABLE}) содержатся дубли. 
Скоринг остановлен. Проверьте модель"""
error_text_compare_with_retro = """Обнаружено падение/увеличение объема результатов скоринга модели. 
Скоринг остановлен. Проверьте модель"""
error_text_no_data = f"""Модель отработала, но результаты не были доставлены в {settings.METRICS_FINAL_TABLE}.
Проверьте модель"""
