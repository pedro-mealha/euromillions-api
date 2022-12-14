from flask import Blueprint, request, jsonify, request
from api import service

bp = Blueprint('api', __name__)

@bp.get('/draws')
def get_draws():
    year = request.args.get('year')
    dates = request.args.get('dates')

    if dates != None:
        dates = dates.split(',')

    results = service.get_draws(year, dates)

    return jsonify(results), 200

@bp.get('/draws/<int:draw_id>')
def get_draw(draw_id):
    contest = service.get_draw(draw_id)

    if contest != None:
        return jsonify(contest), 200

    return "", 404

@bp.get('/')
def index():
    return "Hi there! Have a look at our documentation: https://euromillios-api.readme.io", 200
