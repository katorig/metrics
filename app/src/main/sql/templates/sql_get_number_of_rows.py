def count_rows_with_report_date(table_name,
                                model_id,
                                report_date,
                                retro_date: str = ''):
    if retro_date != '':
        more = retro_date
        less = report_date
    else:
        more = report_date
        less = report_date
    count_rows = f"""
    SELECT Count(*) as cnt, report_date, model_id
    FROM {table_name}
    WHERE model_id = {model_id} AND report_date >= DATE'{more}' AND report_date <= DATE'{less}'
    GROUP BY report_date, model_id
    ;
    """
    return count_rows
