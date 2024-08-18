from flask import render_template, request, jsonify, session, redirect, url_for
from app import app
from app import invest

app.secret_key = 'your_secret_key_here'  # Replace with a real secret key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    session['simulation_params'] = data
    return jsonify({"status": "success"})

@app.route('/run_simulation')
def run_simulation():
    params = session.get('simulation_params')
    if not params:
        return redirect(url_for('index'))

    result_dict = invest.simulate(
        params['etf_symbol'],
        params['start_date'],
        params['end_date'],
        float(params['starting_principal']),
        float(params['auto_invest_amount']),
        params.get('investment_interval'),
        params['frequency']
    )
    session['simulation_result'] = result_dict
    return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/check_result')
def check_result():
    result = session.get('simulation_result')
    if result is not None:
        return jsonify(result)
    else:
        return jsonify({"status": "pending"})