import os
from api.utils.db import Database
from flask import Blueprint, request, jsonify, request, send_from_directory
from api import service, db

bp = Blueprint('api', __name__)

db = Database()

@bp.post('/draws')
def parse_new_draws():
    added = service.parse_new_draws()

    db.close()
    if added:
        return "", 201
    else:
        return jsonify({"error": True}), 400

@bp.get('/draws')
def get_draws():
    year = request.args.get('year')
    dates = request.args.get('dates')

    if dates != None:
        dates = dates.split(',')

    results = service.get_draws(year, dates)
    db.close()

    return jsonify(results), 200

@bp.get('/draws/<int:draw_id>')
def get_draw(draw_id):
    contest = service.get_draw(draw_id)

    db.close()

    if contest != None:
        return jsonify(contest), 200

    return "", 404

@bp.get('/')
def index():
    return "Hi there! Have a look at our documentation: https://euromillios-api.readme.io", 200
