from datetime import date
from api import persistence, external

def get_draws(year: int, dates: list) -> list:
    return persistence.get_draws(year, dates)

def get_draw(draw_id: int) -> list:
    return persistence.get_draw_by_id(draw_id)
