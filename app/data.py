import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime

API_KEY = '4TQMXGUETS7505NZ'
DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
ETF_SYMBOLS = [
    "SPY",
    "QQQ",
    "DIA",
    "VTI",
    "IWM",
    "EFA",
    "VWO",
    "GLD",
    "AGG",
    "TLT",
    "XLF",
    "XLE",
    "VNQ",
    "ARKK",
    "IJH"
]

def fetch_and_store_data(etf_symbols=ETF_SYMBOLS):
    """
    Fetch data for given ETF symbols and store as CSV files.
    """
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    ts = TimeSeries(key=API_KEY, output_format='pandas')

    for symbol in etf_symbols:
        try:
            data, _ = ts.get_daily(symbol=symbol, outputsize='full')
            data.index = pd.to_datetime(data.index)
            data.sort_index(inplace=True)
            
            file_path = os.path.join(DATA_FOLDER, f"{symbol}.csv")
            data.to_csv(file_path)
            print(f"Data for {symbol} has been stored in {file_path}")
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")

def get_local_data(etf_symbol=ETF_SYMBOLS):
    """
    Read data from local storage for a given ETF symbol.
    """
    file_path = os.path.join(DATA_FOLDER, f"{etf_symbol}.csv")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data for {etf_symbol} not found. Please fetch the data first.")
    
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)
    return data

def update_local_data(etf_symbols=ETF_SYMBOLS):
    """
    Update local data for given ETF symbols.
    """
    ts = TimeSeries(key=API_KEY, output_format='pandas')

    for symbol in etf_symbols:
        file_path = os.path.join(DATA_FOLDER, f"{symbol}.csv")
        
        if os.path.exists(file_path):
            local_data = pd.read_csv(file_path, index_col=0, parse_dates=True)
            last_date = local_data.index.max()
            
            try:
                new_data, _ = ts.get_daily(symbol=symbol, outputsize='compact')
                new_data.index = pd.to_datetime(new_data.index)
                new_data = new_data[new_data.index > last_date]
                
                if not new_data.empty:
                    updated_data = pd.concat([local_data, new_data])
                    updated_data.sort_index(inplace=True)
                    updated_data.to_csv(file_path)
                    print(f"Data for {symbol} has been updated")
                else:
                    print(f"Data for {symbol} is already up to date")
            except Exception as e:
                print(f"Error updating data for {symbol}: {str(e)}")
        else:
            print(f"Data for {symbol} not found. Fetching full data...")
            fetch_and_store_data([symbol])
