from dynaconf import settings as envs


def count_rows_for_report_date(table_name):
    q = f"""
    SELECT Count(*) as cnt
    FROM {table_name}
    WHERE model_id = {envs.M_MODEL_ID} AND report_date = DATE'{envs.M_REPORT_DATE}'
    GROUP BY report_date, model_id
    """
    print(q)
    return q


def count_rows_for_retro(table_name,
                         condition):
    if condition == 'retro_df':
        date_expression = f"report_date = DATE'{envs.M_RETRO_DATE}'"
    elif condition == 'retro_df_many_dates':
        date_expression = f"report_date >= DATE'{envs.M_RETRO_DATE}' AND report_date < DATE'{envs.M_REPORT_DATE}'"
    q = f"""
    SELECT Count(*) as cnt
    FROM {table_name}
    WHERE model_id = {envs.M_MODEL_ID} AND {date_expression}
    GROUP BY report_date, model_id
    """
    print(q)
    return q


def count_rows_with_expr(table_name, expression):
    q = f"""
    SELECT Count(*) AS cnt
    FROM {table_name}
    {expression}
    """
    return q


def count_duplicates(table_name, col_name):
    q = f"""
    SELECT Count(*) AS cnt FROM (
        SELECT Count(*) AS cnt
        FROM {table_name}
        GROUP BY {col_name}
        HAVING Cnt > 1 
    ) t
    """
    return q
