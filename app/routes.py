from flask import render_template, request, jsonify
import threading
import uuid
from app import app
from app import invest

RESULTS = {}

@app.route('/')
def index():
    return render_template('index.html')

def simulate_investment(request_id, *args):
    result_dict = invest.simulate(*args)
    RESULTS[request_id] = result_dict

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    etf_symbol = data['etf_symbol']
    start_date = data['start_date']
    end_date = data['end_date']
    starting_principal = float(data['starting_principal'])
    auto_invest_amount = float(data['auto_invest_amount'])
    investment_interval = data.get('investment_interval')
    frequency = data['frequency']

    request_id = str(uuid.uuid4())
    threading.Thread(target=simulate_investment,
                     args=(request_id,
                           etf_symbol,
                           start_date,
                           end_date,
                           starting_principal,
                           auto_invest_amount,
                           investment_interval,
                           frequency
                           )).start()

    return jsonify({"request_id": request_id})

@app.route('/result')
def result():
    request_id = request.args.get('request_id', '')
    return render_template('result.html', request_id=request_id)

@app.route('/check_result')
def check_result():
    request_id = request.args.get('request_id', '')
    result = RESULTS.get(request_id)
    if result is not None:
        return jsonify(result)  # Return the entire result dictionary
    else:
        return jsonify({"status": "pending"})