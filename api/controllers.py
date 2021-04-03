from flask import Blueprint, json, request, jsonify, request

import api.service as service

bp = Blueprint('euromillions_api', __name__)

@bp.route('/results', methods=['POST'])
def parse_new_results_controller():
    added = service.parse_new_results()
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

    return jsonify(service.get_results(year, dates)), 200

@bp.route('/results/<int:contest_id>')
def get_result_controller(contest_id):
    contest = service.get_result(contest_id)
    if contest != None:
        return jsonify(contest), 200

    return "", 404
