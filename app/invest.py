import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import numpy as np

API_KEY = '4TQMXGUETS7505NZ'

def simulate(etf_symbol, start_date, end_date, starting_principal, auto_invest_amount, investment_interval, frequency):
    # Initialize Alpha Vantage API
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    
    # Fetch daily ETF data
    data, meta_data = ts.get_daily(symbol=etf_symbol, outputsize='full')
    
    # Convert the index to datetime format
    data.index = pd.to_datetime(data.index)
    
    # Sort data by date
    data.sort_index(inplace=True)
    
    # Filter data based on the provided date range
    data = data.loc[start_date:end_date]
    
    # Initialize variables
    total_investment = starting_principal
    shares_owned = starting_principal / data['4. close'].iloc[0]
    total_contributions = 0
    
    # Determine the investment dates based on the frequency and interval
    if frequency == 'daily':
        investment_dates = pd.date_range(start=start_date, end=end_date, freq='B')  # Business days
    elif frequency == 'weekly':
        investment_dates = pd.date_range(start=start_date, end=end_date, freq='W-' + investment_interval[:3])
    elif frequency == 'bi-weekly':
        investment_dates = pd.date_range(start=start_date, end=end_date, freq='2W-' + investment_interval[:3])
    elif frequency == 'monthly':
        investment_dates = pd.date_range(start=start_date, end=end_date, freq='M')
    else:
        raise ValueError("Invalid frequency. Options are: 'daily', 'weekly', 'bi-weekly', 'monthly'.")
    
    # Iterate over the investment dates
    for current_date in investment_dates:
        if current_date in data.index:
            # Buy additional shares at the current date price
            price = data.loc[current_date]['4. close']
            new_shares = auto_invest_amount / price
            shares_owned += new_shares
            total_investment += auto_invest_amount
            total_contributions += auto_invest_amount
    
    # Calculate final investment value
    final_price = data.iloc[-1]['4. close']
    final_value = shares_owned * final_price
    
    # Calculate returns
    profit = final_value - total_investment
    profit_percentage_overall = (profit / total_investment) * 100
    
    # Calculate days invested
    days_invested = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
    years_invested = days_invested / 365.25
    
    # Calculate annual return (using CAGR)
    profit_percentage_per_year = ((final_value / total_investment) ** (1 / years_invested) - 1) * 100
    
    # Calculate volatility (standard deviation of daily returns)
    daily_returns = data['4. close'].pct_change().dropna()
    volatility = daily_returns.std() * np.sqrt(252) * 100  # Annualized volatility
    
    # Calculate maximum drawdown
    cumulative_returns = (1 + daily_returns).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min() * 100
    
    # Calculate best and worst year returns
    yearly_returns = data['4. close'].resample('YE').last().pct_change().dropna()
    if len(yearly_returns) > 0:
        best_year_return = yearly_returns.max() * 100
        worst_year_return = yearly_returns.min() * 100
    else:
        # Use profit_percentage_per_year as default when there's insufficient data
        best_year_return = profit_percentage_per_year
        worst_year_return = profit_percentage_per_year
    
    # Calculate Sharpe ratio (assuming risk-free rate of 2%)
    risk_free_rate = 0.02
    sharpe_ratio = (profit_percentage_per_year - risk_free_rate) / volatility
    
    # Calculate Sortino ratio (downside risk)
    negative_returns = daily_returns[daily_returns < 0]
    if len(negative_returns) > 0:
        downside_deviation = np.sqrt(np.mean(negative_returns**2)) * np.sqrt(252) * 100
        if downside_deviation != 0:
            sortino_ratio = (profit_percentage_per_year - risk_free_rate) / downside_deviation
        else:
            sortino_ratio = 0  # No downside deviation
    else:
        sortino_ratio = 0  # No negative returns
    
    return {
        'profit': float(profit),
        'days_invested': int(days_invested),
        'starting_principal': float(starting_principal),
        'total_contributions': float(total_contributions),
        'total_investment': float(total_investment),
        'final_value': float(final_value),
        'profit_percentage_overall': float(profit_percentage_overall),
        'profit_percentage_per_year': float(profit_percentage_per_year),
        'best_year_return': float(best_year_return),
        'worst_year_return': float(worst_year_return),
        'volatility': float(volatility),
        'max_drawdown': float(max_drawdown),
        'sharpe_ratio': float(sharpe_ratio),
        'sortino_ratio': float(sortino_ratio),
    }