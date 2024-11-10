# invest.py
import pandas as pd
import numpy as np
from data import get_local_data
from typing import Dict, Any, Optional
from functools import lru_cache

MAX_DATA_POINTS = 50

@lru_cache(maxsize=10000)
def simulate(etf_symbol: str,
             start_date: str,
             end_date: str,
             starting_principal: float,
             auto_invest_amount: float,
             investment_interval: Optional[str],
             frequency: str) -> Dict[str, Any]:
    """
    Simulate the investment of an ETF over a given date range.

    Args:
        etf_symbol (str): The symbol of the ETF to simulate.
        start_date (str): The start date of the simulation.
        end_date (str): The end date of the simulation.
        starting_principal (float): The starting principal amount.
        auto_invest_amount (float): The amount to invest each time.
        investment_interval (str): The day of the week to invest.
        frequency (str): The frequency of the investment.
    
    Returns:
        Dict[str, Any]: A dictionary containing the simulation results.
        keys:
            profit: float
            days_invested: int
            starting_principal: float
            total_contributions: float
            total_investment: float
            final_value: float
            profit_percentage_overall: float
            profit_percentage_per_year: float
            best_year_return: float
            worst_year_return: float
            volatility: float
            max_drawdown: float
            sharpe_ratio: float
            sortino_ratio: float
            plot_data: Dict[str, list]
                dates: List[str]
                profit_percentages: List[float]
    """
    # Fetch data from local storage
    data = get_local_data(etf_symbol)
    
    # Ensure the index is in datetime format and sorted
    data.index = pd.to_datetime(data.index)
    data = data.sort_index()
    
    # Filter data based on the provided date range
    data = data.loc[start_date:end_date]
    
    if data.empty:
        raise ValueError("No data available for the given date range.")
    
    # Determine the investment dates based on the frequency and interval
    if frequency == 'daily':
        investment_dates = pd.date_range(start=start_date, end=end_date, freq='B')  # Business days
    elif frequency == 'weekly':
        if investment_interval is None:
            raise ValueError("Investment interval is required for weekly frequency.")
        investment_dates = pd.date_range(start=start_date, end=end_date, freq='W-' + investment_interval[:3])
    elif frequency == 'bi-weekly':
        if investment_interval is None:
            raise ValueError("Investment interval is required for bi-weekly frequency.")
        investment_dates = pd.date_range(start=start_date, end=end_date, freq='2W-' + investment_interval[:3])
    elif frequency == 'monthly':
        investment_dates = pd.date_range(start=start_date, end=end_date, freq='ME')
    else:
        raise ValueError("Invalid frequency. Options are: 'daily', 'weekly', 'bi-weekly', 'monthly'.")
    
    # Initialize simulation variables
    total_investment = starting_principal
    initial_price = data['4. close'].iloc[0]
    shares_owned = starting_principal / initial_price
    total_contributions = starting_principal  # Starting principal is also the first contribution
    
    # Lists to store dates and corresponding profit percentages
    profit_percentage_list = []
    plot_dates = []
    
    # Initialize with the start date and 0% profit
    first_date = data.index[0]
    profit_percentage_list.append(0.0)
    plot_dates.append(first_date.strftime('%Y-%m-%d'))
    
    # Iterate over each day in the data to track cumulative investment and portfolio value
    for current_date in data.index:
        # Check if today is an investment day
        if current_date in investment_dates:
            price = data.loc[current_date]['4. close']
            if price <= 0:
                raise ValueError(f"Invalid price on {current_date.strftime('%Y-%m-%d')}: {price}")
            new_shares = auto_invest_amount / price
            shares_owned += new_shares
            total_investment += auto_invest_amount
            total_contributions += auto_invest_amount
        
        # Calculate current portfolio value
        current_price = data.loc[current_date]['4. close']
        current_value = shares_owned * current_price
        
        # Calculate profit percentage
        profit = current_value - total_investment
        profit_percentage = (profit / total_investment) * 100
        profit_percentage_list.append(profit_percentage)
        plot_dates.append(current_date.strftime('%Y-%m-%d'))
    
    # Calculate final values after the loop
    final_price = data.iloc[-1]['4. close']
    final_value = shares_owned * final_price
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
    risk_free_rate = 2.0  # Already in percentage
    sharpe_ratio = (profit_percentage_per_year - risk_free_rate) / volatility if volatility != 0 else 0
    
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
    
    # Generate plot data: profit percentage over time
    # Ensure that we have at least one data point
    if len(profit_percentage_list) == 0:
        plot_data = {
            'dates': [],
            'profit_percentages': []
        }
    else:
        # Sample up to MAX_DATA_POINTS uniformly spaced datapoints
        num_points = min(MAX_DATA_POINTS, len(profit_percentage_list))
        sampled_indices = np.linspace(0, len(profit_percentage_list) - 1, num=num_points, dtype=int)
        sampled_dates = [plot_dates[i] for i in sampled_indices]
        sampled_profit_percentages = [round(profit_percentage_list[i], 2) for i in sampled_indices]
        
        plot_data = {
            'dates': sampled_dates,
            'profit_percentages': [float(p) for p in sampled_profit_percentages]
        }
    
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
        'plot_data': plot_data
    }