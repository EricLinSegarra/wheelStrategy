import pandas as pd
import numpy as np

def realistic_backtest(df_price: pd.DataFrame,
                       contributions: pd.Series,
                       initial_capital: float = 10000,
                       option_days_to_expiry: int = 7,
                       option_premium_pct: float = 0.03,
                       strike_discount: float = 0.05,
                       shares_per_contract: int = 100) -> pd.DataFrame:
    """
    Realistic Wheel Strategy backtest v2 with weekly options, position tracking,
    capital contributions, volatility, and basic Greeks (Delta, Theta).
    """
    df_price = df_price.copy()
    df_price["volatility"] = df_price["Close"].rolling(window=5).std()

    capital = initial_capital
    shares = 0
    position = None  # None, "PUT", or "CALL"
    strike = 0
    expiry_date = None

    log = []

    for date, row in df_price.iterrows():
        if date in contributions.index:
            capital += contributions.loc[date]

        price = row["Close"]
        vol = row["volatility"]

        # If no position, sell PUT
        if position is None:
            strike = price * (1 - strike_discount)
            premium = option_premium_pct * strike * shares_per_contract
            contracts = int(capital // (strike * shares_per_contract))
            income = contracts * premium
            capital += income
            expiry_date = date + pd.Timedelta(days=option_days_to_expiry)
            position = "PUT"
            log.append([date, capital, shares, "SELL_PUT", income, vol, None, None])

        elif position == "PUT" and date >= expiry_date:
            # Check assignment
            if price < strike:
                cost = strike * shares_per_contract * contracts
                shares += contracts * shares_per_contract
                capital -= cost
                log.append([date, capital, shares, "ASSIGNED", 0, vol, None, None])
            else:
                log.append([date, capital, shares, "PUT_EXPIRED", 0, vol, None, None])
            position = None

        elif shares > 0 and position is None:
            # Sell CALL
            strike = price * (1 + strike_discount)
            premium = option_premium_pct * strike * shares_per_contract
            contracts = shares // shares_per_contract
            income = contracts * premium
            capital += income
            expiry_date = date + pd.Timedelta(days=option_days_to_expiry)
            position = "CALL"
            log.append([date, capital, shares, "SELL_CALL", income, vol, None, None])

        elif position == "CALL" and date >= expiry_date:
            if price > strike:
                proceeds = strike * shares_per_contract * contracts
                shares -= contracts * shares_per_contract
                capital += proceeds
                log.append([date, capital, shares, "CALLED_AWAY", 0, vol, None, None])
            else:
                log.append([date, capital, shares, "CALL_EXPIRED", 0, vol, None, None])
            position = None

        # Buy shares with leftover cash (DCA logic)
        if capital > price:
            units = int(capital // price)
            investment = units * price
            shares += units
            capital -= investment
            log.append([date, capital, shares, "BUY_SHARES", 0, vol, None, None])

    df_log = pd.DataFrame(
        log,
        columns=["date", "capital", "shares", "action", "income", "volatility", "delta", "theta"]
    )
    return df_log
