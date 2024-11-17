from flask import Blueprint, request, request
from api import service
from api.utils.db import Database

bp = Blueprint('api', __name__)

# DEPRECATED in favour of GET v1/draws
@bp.get('/draws')
def get_draws():
    db = Database()
    year = request.args.get('year')
    dates = request.args.get('dates')

    if dates != None:
        dates = dates.split(',')

    results = service.get_draws(db, year, dates)

    db.close()
    return results, 200

# DEPRECATED in favour of GET v1/draws/:draw_id
@bp.get('/draws/<int:draw_id>')
def get_draw(draw_id):
    db = Database()
    contest = service.get_draw(db, draw_id)
    db.close()

    if contest != None:
        return contest, 200

    return "", 404

@bp.get('/v1/draws')
def get_draws_v1():
    db = Database()
    year = request.args.get('year')
    dates = request.args.get('dates')
    order_by = request.args.get('order_by')
    limit = request.args.get('limit')

    if dates != None:
        dates = dates.split(',')

    results = service.get_draws_v1(db, year, dates, limit, order_by)

    db.close()
    return results, 200

@bp.get('/v1/draws/<int:draw_id>')
def get_draw_v1(draw_id):
    db = Database()
    contest = service.get_draw_v1(db, draw_id)
    db.close()

    if contest != None:
        return contest, 200

    return "", 404

@bp.get('/')
def index():
    return "Hi there! Have a look at our documentation: https://euromillios-api.readme.io", 200
