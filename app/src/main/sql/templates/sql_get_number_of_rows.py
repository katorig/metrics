def count_rows_for_report_date(table_name,
                               model_id,
                               report_date):
    q = f"""
    SELECT Count(*) as cnt
    FROM {table_name}
    WHERE model_id = {model_id} AND report_date = DATE'{report_date}'
    GROUP BY report_date, model_id
    """
    print(q)
    return q


def count_rows_for_retro(table_name,
                         model_id,
                         retro_date,
                         report_date: str = None):
    date_expression = f"report_date >= DATE'{retro_date}' AND report_date < DATE'{report_date}'"
    q = f"""
    SELECT Count(*) as cnt
    FROM {table_name}
    WHERE model_id = {model_id} AND {date_expression}
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
