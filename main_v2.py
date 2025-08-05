import pandas as pd
import matplotlib.pyplot as plt

from source.engine.backtest_engine_v2 import realistic_backtest
from source.engine.buy_and_hold import buy_and_hold_strategy
from source.data.contribution_schedule import generate_contributions

# --- Parameters ---
ticker = "SOXL"
data_path = f"data/{ticker}_daily.parquet"
start_date = "2010-01-01"
end_date = "2025-07-31"
monthly_contribution = 500
initial_capital = 5000

# --- Load price data ---
df_price = pd.read_parquet(data_path)
df_price.index = pd.to_datetime(df_price.index)
df_price = df_price.loc[start_date:end_date]

# --- Generate contributions ---
contributions = generate_contributions(start_date, end_date, monthly_contribution)
print(contributions)

# --- Run backtest ---
df_result = buy_and_hold_strategy(df_price, contributions, initial_capital=initial_capital)

# --- Save or visualize ---
df_result.to_csv(f"data/{ticker}_backtest_results.csv", index=False)

# --- Plot capital over time ---
df_result.set_index("date")["capital"].plot(figsize=(12, 5), title=f"{ticker} – Capital Evolution")
plt.ylabel("USD")
plt.grid()
plt.tight_layout()
plt.show()
