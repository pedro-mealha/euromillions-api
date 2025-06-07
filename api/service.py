from api import persistence
from api.utils.db import Database

def get_draws(db: Database, year: int, dates: list) -> list:
    return persistence.get_draws(db, year, dates)

def get_draw(db: Database, draw_id: int) -> list:
    return persistence.get_draw_by_id(db, draw_id)

def get_draws_v1(db: Database, year: int = None, dates: list = None, limit: int = None, order_by: list = None) -> list:
    return persistence.get_draws_with_prizes(db, year, dates, limit, order_by)

def get_draw_v1(db: Database, draw_id: int) -> list:
    return persistence.get_draw_with_prizes_by_id(db, draw_id)
