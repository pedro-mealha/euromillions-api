from api import db

def get_results(year: int, dates: list, limit = None, orderBy = None) -> list:
    sql = "SELECT * FROM results"
    vars = []

    if year != None:
        sql, vars = add_condition(sql, vars, 'date_part(\'year\', date) = %s', year)

    if dates != None and len(dates) > 0 and dates[0] != "":
        sql, vars = add_condition(sql, vars, 'date >= %s', dates[0])

    if dates != None and len(dates) > 1 and dates[1] != "":
        sql, vars = add_condition(sql, vars, 'date <= %s', dates[1])

    if orderBy != None and len(orderBy) > 0:
        sql += " ORDER BY %s " % orderBy[0]
        if len(orderBy) > 1 and (orderBy[1] == "ASC" or orderBy[1] == "DESC"):
            sql += orderBy[1]

    if limit != None and limit > 0:
        sql += ' LIMIT %s'
        vars.append(limit)

    db.getCursor().execute(sql, vars)
    results = db.getCursor().fetchall()

    return results

def get_latest_result() -> dict:
    latest = get_results(None, None, 1, ["id", "DESC"])
    if len(latest) > 0:
        return latest[0]

    return None

def get_result_by_id(contest_id: int) -> list:
    sql = "SELECT * FROM results WHERE contest_id = %s"

    db.getCursor().execute(sql, [contest_id])
    result = db.getCursor().fetchone()

    return result

def insert_contests(contests: list) -> bool:
    sql = "INSERT INTO results (contest_id, numbers, stars, date, prize, has_winner) VALUES "
    vars = []
    for index, contest in enumerate(contests):
        if index == 0:
            sql += "(%s, %s, %s, %s, %s, %s)"
        else:
            sql += ", (%s, %s, %s, %s, %s, %s)"

        vars.extend(contest)

    db.getCursor().execute(sql, vars)
    db.commit()

    return True

def add_condition(sql: str, vars: list, condition: str, value) -> list:
    if len(vars) == 0 or 'WHERE' not in sql:
        sql += " WHERE "
    else:
        sql += " AND "

    vars.append(value)
    sql += condition

    return [sql, vars]
