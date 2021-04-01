from flask import Flask, request, jsonify
import service

app = Flask(__name__)

@app.route('/results', methods=['POST'])
def results():
    return {}

@app.route('/results', methods=['GET'])
def get_results_controller():
    year = request.args.get('year')
    dates = request.args.get('dates').split(',')

    return jsonify(service.get_results(year, dates))

@app.route('/results/<int:contest_id>')
def get_result_controller(contest_id):
    return jsonify(service.get_result(contest_id))
