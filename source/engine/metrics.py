import pandas as pd
import numpy as np


def cagr(series: pd.Series, freq_per_year=252) -> float:
    if len(series) < 2: return 0.0
    start, end = float(series.iloc[0]), float(series.iloc[-1])
    years = len(series) / freq_per_year
    return (end / start) ** (1/years) - 1 if start > 0 else np.nan


def max_drawdown(series: pd.Series) -> float:
    roll_max = series.cummax()
    dd = series / roll_max - 1.0
    return float(dd.min())



def annual_vol(series: pd.Series, freq_per_year=252) -> float:
    ret = series.pct_change().dropna()
    return float(ret.std() * np.sqrt(freq_per_year))

def sharpe(series: pd.Series, rf=0.0, freq_per_year=252) -> float:
    ret = series.pct_change().dropna()
    excess = ret - rf / freq_per_year
    mu = excess.mean() * freq_per_year
    sig = ret.std() * np.sqrt(freq_per_year)
    return float(mu / sig) if sig > 0 else np.nan
