df_from_prd_table = """
SELECT * 
FROM {0}
WHERE model_id = {1}
AND report_date = date'{2}'
;
"""

count_rows_in_prd_table = """
SELECT Count(*) as cnt, report_date, model_id
FROM {0}
WHERE model_id = {1} AND report_date = date'{2}'
GROUP BY report_date, model_id
;
"""


retro_df_from_prd_table = """
SELECT Count(*) as cnt, report_date, model_id
FROM prd2_dds_v.scoring
WHERE model_id = {0} AND report_date >= Add_Months(date'{1}', -3)
GROUP BY report_date, model_id
;
"""