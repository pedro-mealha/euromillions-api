from utils.db import Database

def get_results(year: int, dates: list) -> dict:
    db = Database()
    sql = "SELECT * FROM results"
    vars = []

    if year != None:
        sql, vars = add_condition(sql, vars, 'date_part(\'year\', date) = %s', year)

    if len(dates) > 0 and dates[0] != None and dates[0] != "":
        sql, vars = add_condition(sql, vars, 'date >= %s', dates[0])

    if len(dates) > 1 and dates[1] != None and dates[1] != "":
        sql, vars = add_condition(sql, vars, 'date <= %s', dates[1])

    db.getCursor().execute(sql, vars)
    results = db.getCursor().fetchall()
    db.close()

    return results

def get_result_by_id(contest_id: int) -> list:
    db = Database()
    sql = "SELECT * FROM results WHERE contest_id = %s"

    db.getCursor().execute(sql, [contest_id])
    result = db.getCursor().fetchone()
    db.close()

    return result

def add_condition(sql: str, vars: list, condition: str, value) -> list:
    if len(vars) == 0 or 'WHERE' not in sql:
        sql = sql + " WHERE "
    else:
        sql = sql + " AND "

    vars.append(value)
    sql = sql + condition

    return [sql, vars]
