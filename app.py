# app.py
from flask import Flask, render_template, request, jsonify, session
import invest

app = Flask(__name__)
app.secret_key = "secret"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.get_json()
        etf_symbol = data.get('etf_symbol')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        starting_principal = float(data.get('starting_principal', 0))
        auto_invest_amount = float(data.get('auto_invest_amount', 0))
        investment_interval = data.get('investment_interval', '')
        frequency = data.get('frequency')

        if not all([etf_symbol, start_date, end_date, starting_principal, auto_invest_amount, frequency]):
            return jsonify({'error': 'Missing required parameters.'}), 400

        # Call the simulate function
        result = invest.simulate(
            etf_symbol=etf_symbol,
            start_date=start_date,
            end_date=end_date,
            starting_principal=starting_principal,
            auto_invest_amount=auto_invest_amount,
            investment_interval=investment_interval,
            frequency=frequency
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/compare', methods=['GET'])
def compare():
    return render_template('compare.html')

@app.route('/set_base', methods=['POST'])
def set_base():
    try:
        data = request.get_json()
        new_base_params = data.get('new_base_params')

        if not new_base_params:
            return jsonify({'error': 'No base parameters provided.'}), 400

        # Save the new base parameters in the session
        session['base_params'] = new_base_params

        return jsonify({'message': 'Base parameters updated.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_base', methods=['GET'])
def get_base():
    try:
        base_params = session.get('base_params')
        if not base_params:
            return jsonify({'error': 'No base investment parameters found.'}), 400
        return jsonify({'base_params': base_params}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)