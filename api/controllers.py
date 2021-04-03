from flask import Blueprint, request, jsonify, request

from api import service, db

bp = Blueprint('api', __name__)

@bp.route('/draws', methods=['POST'])
def parse_new_draws():
    added = service.parse_new_draws()

    db.close()
    if added:
        return "", 201
    else:
        return jsonify({"error": True}), 400

@bp.route('/draws', methods=['GET'])
def get_draws():
    year = request.args.get('year')
    dates = request.args.get('dates')

    if dates != None:
        dates = dates.split(',')

    results = service.get_draws(year, dates)
    db.close()

    return jsonify(results), 200

@bp.route('/draws/<int:draw_id>')
def get_draw(draw_id):
    contest = service.get_draw(draw_id)

    db.close()

    if contest != None:
        return jsonify(contest), 200

    return "", 404
