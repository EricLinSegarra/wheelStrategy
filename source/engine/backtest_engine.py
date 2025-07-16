import pandas as pd

def simple_backtest(
    df_price: pd.DataFrame,
    contributions: pd.Series,
    strike_discount: float = 0.05,
    option_premium_pct: float = 0.03,
    initial_capital: float = 5000
) -> pd.DataFrame:
    """
    Simulates the Wheel Strategy with fixed monthly contributions.

    Parameters:
        df_price (pd.DataFrame): OHLC data with a DateTimeIndex
        contributions (pd.Series): Monthly capital injections
        strike_discount (float): Discount from market price for PUT strike
        option_premium_pct (float): Option premium as % of strike
        initial_capital (float): Starting capital

    Returns:
        pd.DataFrame: Backtest results with capital and income per month
    """
    capital = initial_capital
    history = []

    for date, row in df_price.iterrows():
        if date not in contributions.index:
            continue  # Skip if no contribution on this date

        capital += contributions.loc[date]

        # Ensure scalar value from row
        close_price = row["Close"].item() if hasattr(row["Close"], "item") else row["Close"]

        strike = close_price * (1 - strike_discount)
        premium = option_premium_pct * strike * 100

        n_contracts = int(capital // (strike * 100))
        income = n_contracts * premium
        capital += income

        history.append((date, capital, income))

    return pd.DataFrame(history, columns=["date", "capital", "income"])
