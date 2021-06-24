#!/bin/bash

kinit -kt ../../secrets/ekaterina.gruzdova.keytab ekaterina.gruzdova@CORP.TELE2.RU

#cd /opt/conda/envs/app-env/lib/python3.7/site-packages/tele2_metrics/
cd ../tele2_metrics
chmod +x tele2_metrics.py
./tele2_metrics.py --help
./tele2_metrics.py compare_new_df_with_retro --notify 1 --model_id 135 --stage_db 'hadoop' \
--stage_table 'developers.eg_msg_traf_1' --final_db 'teradata' --final_table 'prd2_dds_v.scoring' \
--retro_type 'retro_df_many_dates' --threshold 15 --retro_date '2021-03-04' --report_date '2021-06-04' \
--send_to 'ekaterina.gruzdova@tele2.ru'
if [ $? -eq 0 ]; then
  ./tele2_metrics.py check_df_for_duplicates --notify 1 --model_id 135 --stage_db 'hadoop' \
  --stage_table 'developers.eg_msg_traf_1' --column 'segment_id,subs_id' --send_to 'ekaterina.gruzdova@tele2.ru'
else
  echo 'FAIL'
  exit 1
fi

./tele2_metrics.py check_if_data_in_table --model_id 135 --final_db 'teradata' \
--final_table 'prd2_dds_v.scoring' --report_date '2021-06-04' --send_to 'ekaterina.gruzdova@tele2.ru' --notify 1
