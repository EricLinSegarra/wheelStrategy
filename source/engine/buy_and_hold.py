import pandas as pd


def buy_and_hold_strategy(prices: pd.DataFrame,
                          contributions: pd.Series,
                          initial_capital: float) -> pd.DataFrame:
    """
    prices: DataFrame con columna 'Close' y DateTimeIndex (días de mercado)
    contributions: Series con aportes (índice de fecha). Se ajusta al día de mercado anterior (asof).
    """
    prices = prices.copy()
    prices.index = pd.to_datetime(prices.index)

    # Alinea contribuciones al calendario de mercado (asof -> último día hábil <= fecha)
    contrib = contributions.sort_index().astype(float)
    contrib_on_trading_days = pd.Series(0.0, index=prices.index)
    contrib_on_trading_days.loc[contrib.index] = contrib.values
    contrib_on_trading_days = contrib_on_trading_days.asfreq("D", method=None).reindex(prices.index, fill_value=0.0)

    records = []
    shares = 0
    cash = float(initial_capital)

    for date, row in prices.iterrows():
        price = float(row["Close"])

        # aporte (si lo hay) este día de mercado
        cash += float(contrib_on_trading_days.loc[date])

        # comprar el máximo de acciones enteras
        if price > 0 and cash >= price:
            new_shares = int(cash // price)
            cash -= round(new_shares * price, 2)
            shares += new_shares

        portfolio_value = shares * price + cash
        records.append({
            "date": date,
            "action": "BUY" if new_shares > 0 else "HOLD",
            "shares": shares,
            "price": price,
            "free_cash": cash,
            "capital": portfolio_value
        })

    return pd.DataFrame(records)
