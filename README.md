# ETF Investment Simulator

![image-20240714125756713](https://github.com/AnJunHao/etf-investment-simulator/blob/main/README.assets/image-20240714125756713.png?raw=true)

![image-20240714125831795](https://github.com/AnJunHao/etf-investment-simulator/blob/main/README.assets/image-20240714125831795.png?raw=true)

## Project Description

This Flask-based web application simulates ETF (Exchange-Traded Fund) investments over a specified time period. It allows users to input various parameters such as ETF symbol, date range, initial investment, and periodic investment amounts. The application then calculates and displays key investment metrics including total returns, annualized returns, volatility, and risk-adjusted performance measures.

## Features

- Simulate ETF investments with customizable parameters
- Calculate key investment metrics:
  - Total profit/loss
  - Overall and annualized returns
  - Investment volatility
  - Maximum drawdown
  - Sharpe and Sortino ratios
- Asynchronous processing for long-running simulations
- Interactive web interface

## Installation

1. Clone the repository:
```
   git clone https://github.com/AnJunHao/etf-investment-simulator.git
   cd etf-investment-simulator
```

2. Create a virtual environment and activate it:
   ```
   python -m venv etf-investment-simulator
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your Alpha Vantage API key:
   - Sign up for a free API key at [Alpha Vantage](https://www.alphavantage.co/)
   - Replace the `API_KEY` in `app/invest.py` with your actual API key

## Usage

1. Start the Flask development server:
   ```
   flask run
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Use the web interface to input your investment parameters:
   - ETF Symbol (e.g., SPY for S&P 500 ETF)
   - Start and End dates for the investment period
   - Initial investment amount
   - Periodic investment amount and frequency

4. Submit the form to run the simulation

5. View the results, including various investment performance metrics

## Project Structure

   ```
project_root/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── invest.py
│   ├── templates/
│   │   ├── index.html
│   │   └── result.html
│   └── static/
│       ├── js/
│       └── css/
├── data/
│   └── (CSV files for each ETF will be stored here)
├── run.py
├── .flaskenv
├── requirements.txt
└── README.md
   ```

## Dependencies

- Flask: Web framework
- Pandas: Data manipulation and analysis
- Alpha Vantage: API for fetching stock data
- NumPy: Numerical computing
- python-dotenv: Loading environment variables

For a complete list of dependencies and their versions, see `requirements.txt`.

## Configuration

The application uses a `.flaskenv` file for Flask configuration. You can modify this file to change Flask environment settings.

## Disclaimer

This application is for educational purposes only. It does not constitute financial advice. Always consult with a qualified financial advisor before making investment decisions.
