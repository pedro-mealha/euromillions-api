from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        return {}
    else:
        year = request.args.get('year')
        dates = request.args.get('dates')
        return jsonify([{
            "year": year,
            "dates": dates,
        }])

@app.route('/results/<int:result_id>')
def result(result_id):
    return {
        "id": result_id
    }
