from api import db

def get_draws(year: int, dates: list, limit = None, orderBy = ["date", "ASC"]) -> list:
    sql = "SELECT * FROM draws"
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
    draws = db.getCursor().fetchall()

    return draws

def get_latest_draw() -> dict:
    latest = get_draws(None, None, 1, ["date", "DESC"])
    if len(latest) > 0:
        return latest[0]

    return None

def get_draw_by_id(draw_id: int) -> list:
    sql = "SELECT * FROM draws WHERE draw_id = %s"

    db.getCursor().execute(sql, [draw_id])
    draw = db.getCursor().fetchone()

    return draw

def insert_draws(draws: list) -> bool:
    sql = "INSERT INTO draws (draw_id, numbers, stars, date, prize, has_winner) VALUES "
    vars = []
    for i, draw in enumerate(draws):
        if i == 0:
            sql += "(%s, %s, %s, %s, %s, %s)"
        else:
            sql += ", (%s, %s, %s, %s, %s, %s)"

        vars.extend(draw)

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
