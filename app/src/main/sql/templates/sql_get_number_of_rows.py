def count_rows_for_report_date(table_name,
                               model_id,
                               report_date):
    count_rows = f"""
    SELECT Count(*) as cnt
    FROM {table_name}
    WHERE model_id = {model_id} AND report_date = DATE'{report_date}'
    GROUP BY report_date, model_id
    """
    print(count_rows)
    return count_rows


def count_rows_for_retro(table_name,
                         model_id,
                         retro_date,
                         report_date: str = None):
    if report_date:
        date_expression = f"report_date >= DATE'{retro_date}' AND report_date < DATE'{report_date}'"
    elif report_date is None:
        date_expression = f"report_date = DATE'{retro_date}'"
    count_rows = f"""
    SELECT Count(*) as cnt
    FROM {table_name}
    WHERE model_id = {model_id} AND {date_expression}
    GROUP BY report_date, model_id
    """
    print(count_rows)
    return count_rows


def count_duplicates(table_name, col_name):
    query = f"""
    SELECT count(*) FROM (
    SELECT Count(*) AS cnt
    FROM {table_name}
    GROUP BY {col_name}
    HAVING Cnt > 1 ) t
    """
    return query
