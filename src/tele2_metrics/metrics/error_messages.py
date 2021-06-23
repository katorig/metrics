from dynaconf import settings

error_text_duplicates = f"""В результатах скоринга модели (таблица {settings.METRICS_STAGE_TABLE}) содержатся дубли за report_date {settings.METRICS_REPORT_DATE}. 
Скоринг остановлен. Проверьте модель"""
error_text_compare_with_retro = f"""Обнаружено аномальное количество скоров в результатах модели за report_date {settings.METRICS_REPORT_DATE}. 
Скоринг остановлен. Проверьте модель"""
error_text_no_data = f"""Модель отработала, но результаты не были доставлены в {settings.METRICS_FINAL_TABLE} за report_date {settings.METRICS_REPORT_DATE}.
Проверьте модель"""
