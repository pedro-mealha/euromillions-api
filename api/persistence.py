from api.utils.db import Database

def get_draws(db: Database, year: int, dates: list, limit = None, orderBy = ["date", "ASC"]) -> list:
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

    return db.getConn().execute(sql, vars).fetchall()

def get_latest_draw(db: Database) -> dict:
    latest = get_draws(db, None, None, 1, ["date", "DESC"])
    if len(latest) > 0:
        return latest[0]

    return None

def get_draw_by_id(db: Database, draw_id: int) -> list:
    sql = "SELECT * FROM draws WHERE draw_id = %s"

    return db.getConn().execute(sql, [draw_id]).fetchone()

def get_prize_combinations(db: Database) -> list:
    sql = "SELECT * FROM prize_combinations"

    return db.getConn().execute(sql).fetchall()

def insert_draws(db: Database, draws: list) -> bool:
    sql = "INSERT INTO draws (draw_id, numbers, stars, date, prize, has_winner) VALUES "
    vars = []
    for i, draw in enumerate(draws):
        if i == 0:
            sql += "(%s, %s, %s, %s, %s, %s)"
        else:
            sql += ", (%s, %s, %s, %s, %s, %s)"

        vars.extend(draw)

    db.getConn().execute(sql, vars)
    db.commit()

    return True

def insert_draws_prizes(db: Database, draws_prizes: list) -> bool:
    sql = "INSERT INTO draws_prizes (draw_id, prize_combination_id, prize, winners) VALUES "
    vars = []
    for i, draw_prizes in enumerate(draws_prizes):
        if i == 0:
            sql += "(%s, %s, %s, %s)"
        else:
            sql += ", (%s, %s, %s, %s)"

        vars.extend(draw_prizes)

    db.getConn().execute(sql, vars)
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
