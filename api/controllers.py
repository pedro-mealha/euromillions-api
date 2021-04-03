from flask import Blueprint, request, jsonify, request

from api import service, db

bp = Blueprint('api', __name__)

@bp.route('/results', methods=['POST'])
def parse_new_results_controller():
    added = service.parse_new_results()

    db.close()
    if added:
        return "", 201
    else:
        return jsonify({"error": True}), 400

@bp.route('/results', methods=['GET'])
def get_results_controller():
    year = request.args.get('year')
    dates = request.args.get('dates')

    if dates != None:
        dates = dates.split(',')

    results = service.get_results(year, dates)
    db.close()

    return jsonify(results), 200

@bp.route('/results/<int:contest_id>')
def get_result_controller(contest_id):
    contest = service.get_result(contest_id)

    db.close()

    if contest != None:
        return jsonify(contest), 200

    return "", 404
