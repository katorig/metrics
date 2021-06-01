load_df = """
SELECT * 
FROM {0}
WHERE model_id = {1}
AND report_date = date'{2}'
;
"""
