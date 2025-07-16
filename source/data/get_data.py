import yfinance as yf
import pandas as pd
import os

def download_ohlc_data(ticker="SPY"):
    # Download historical OHLC data
    data = yf.download(ticker, start="1980-01-01", end="2050-07-16", auto_adjust=True)

    # Flatten multi-level columns if present
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(1)

    # Rename columns to standard names
    data.columns = ["Close", "High", "Low", "Open", "Volume"]

    # Save to "data/" directory relative to the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    output_path = os.path.join(project_root, "data", f"{ticker}_daily.parquet")
    print("Saving file to: ", output_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data.to_parquet(output_path)
    return data

if __name__ == "__main__":
    df = download_ohlc_data()
    print("First rows of the dataset:")
    print(df.head())
    print("Last rows of the dataset:")
    print(df.tail())
    print(f"Date range: {df.index.min().date()} to {df.index.max().date()}")
