from dotenv.main import load_dotenv
from flask import Flask, request, jsonify, Response

import app.service as service

app = Flask(__name__)
load_dotenv()

@app.route('/results', methods=['POST'])
def parse_new_results_controller():
    added = service.parse_new_results()
    if added:
        return "", 201
    else:
        return Response("{\"error\":true}", status=400, mimetype='application/json')

@app.route('/results', methods=['GET'])
def get_results_controller():
    year = request.args.get('year')
    dates = request.args.get('dates')

    if dates != None:
        dates = dates.split(',')

    return jsonify(service.get_results(year, dates)), 200

@app.route('/results/<int:contest_id>')
def get_result_controller(contest_id):
    contest = service.get_result(contest_id)
    if contest != None:
        return jsonify(contest), 200

    return "", 404
