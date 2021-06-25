# tele2-metrics

## Фреймворк, предназначенный для метрик и мониторинга качества данных, моделей и результатов скоринга.

Фреймворк можно использовать 
как в виде самостотельной питоновской **библиотеки**,
так и в виде **bash-утилиты**.

На данный момент, артефакт фреймворка лежит на Nexus. 
Если хотите внести изменения в этот проект и переопубликовать его на Nexus,
то поменяйте версию в `src/__init__.py`, а затем запустите файл 
`how_to_send_to_nexus.sh`, предварительно указав NEXUS_USER и NEXUS_PASSWORD.

Установить библиотеку можно при помощи команды 
`pip install tele2-metrics --index-url http://nexus.t2ru-bda-wds-008.corp.tele2.ru/repository/pypi-all/simple --trusted-host nexus.t2ru-bda-wds-008.corp.tele2.ru`
предварительно установив все зависимости, описанные в environment.yml. 
Либо добавить установку библиотеки в сам environment.yml


Перед использованием фреймворка необходимо 
**авторизовать свой keytab** и добавить в окружение 
**переменные TERADATA_USER и TERADATA_PASSWORD**.

Пример вызова и использования утилиты лежит в `tests/test_run.sh`
Для просмотра описания аргументов, возможных для передачи
при запуске утилиты, вызывайте `./tele2_metrics.py --help`

Пример вызова методов в коде на Python написан в `tests/test_metrics.py`
Как видно в примере, перед вызовом метода необходимо обогатить
settings (dynaconf) нужными параметрами, в формате `settings.METRICS_STAGE_DB = 'teradata'`. Также необходимо добавлять settings.toml с переменными dynaconf в проект модели (пример лежит в config/settings.toml), если используется фреймворк в качестве библиотеки прямо в коде.

Пока что не подключена возможность использования teradata по ldap и не было тестирования в Windows. В скором времени исправим.

Доступные метрики на данный момент:
- `compare_new_df_with_retro` (метрика по измерению падения/увеличения объема скоров)\
  Переменные: 
  - METRICS_MODEL_ID
  - METRICS_STAGE_DB
  - METRICS_STAGE_TABLE
  - METRICS_FINAL_DB
  - METRICS_RETRO_TYPE
  - METRICS_FINAL_TABLE
  - METRICS_THRESHOLD
  - METRICS_RETRO_DATE
  - METRICS_REPORT_DATE
  - METRICS_SEND_TO - опционально
- `check_if_data_in_table` (метрика по проверке поступления данных в таблицу)\
  Переменные:
  - METRICS_MODEL_ID
  - METRICS_FINAL_DB
  - METRICS_FINAL_TABLE
  - METRICS_REPORT_DATE
  - METRICS_SEND_TO - опционально
- `check_df_for_duplicates` (метрика по проверке данных на наличие дублей)\
  Переменные:
  - METRICS_MODEL_ID
  - METRICS_FINAL_DB
  - METRICS_FINAL_TABLE
  - METRICS_REPORT_DATE
  - METRICS_SEND_TO - опционально

При возникновении вопросов пишите Кате Груздовой в слаке или на имейл: ekaterina.gruzdova@tele2.ru 
