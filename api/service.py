from api import persistence
from api.utils.db import Database

def get_draws(db: Database, year: int, dates: list) -> list:
    return persistence.get_draws(db, year, dates)

def get_draw(db: Database, draw_id: int) -> list:
    return persistence.get_draw_by_id(db, draw_id)
