#!/bin/bash

kinit -kt ../../../secrets/ekaterina.gruzdova.keytab ekaterina.gruzdova@CORP.TELE2.RU

export DYNACONF_METRICS_MODEL_ID=135
export DYNACONF_METRICS_STAGE_DB='hadoop'
export DYNACONF_METRICS_STAGE_TABLE='developers.eg_msg_traf_1'
export DYNACONF_METRICS_FINAL_DB='teradata'
export DYNACONF_METRICS_FINAL_TABLE='prd2_dds_v.scoring'
export DYNACONF_METRICS_REPORT_DATE='2021-06-04'
export DYNACONF_METRICS_RETRO_DATE='2021-03-04'
export DYNACONF_METRICS_THRESHOLD=15
export DYNACONF_METRICS_COLUMN='subs_id'
export DYNACONF_METRICS_SEND_TO='ekaterina.gruzdova@tele2.ru'
export DYNACONF_METRICS_RETRO_TYPE='retro_df_many_dates'

cd ../main
chmod +x tele2_metrics.py
./tele2_metrics.py compare_new_df_with_retro --notify 1
./tele2_metrics.py check_df_for_duplicates --notify 1
./tele2_metrics.py check_if_data_in_table
