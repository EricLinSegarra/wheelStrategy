import pandas as pd
import matplotlib.pyplot as plt
import os

from source.data.contribution_schedule import generate_contributions
from source.engine.backtest_engine import simple_backtest

# Path to the SOXL dataset (must exist in /data)
ticker = "SPY"
data_path = os.path.join(os.path.dirname(__file__), "data", f"{ticker}_daily.parquet")

# Load OHLC data
df_price = pd.read_parquet(data_path)

# Ensure datetime index
df_price.index = pd.to_datetime(df_price.index)

# Generate $500 monthly contributions from the start to the end of dataset
start_date = df_price.index.min().strftime("%Y-%m-%d")
end_date = df_price.index.max().strftime("%Y-%m-%d")
contributions = generate_contributions(start_date, end_date, monthly_amount=500)

# Run basic Wheel strategy simulation
result = simple_backtest(df_price, contributions)

# Show results
print("📊 Backtest result (last 5 rows):")
print(result.tail())

# Plot capital evolution
plt.figure(figsize=(10, 5))
result.set_index("date")["capital"].plot(
    title=f"📈 Accumulated Capital – {ticker} Wheel Strategy",
    ylabel="Capital [$]",
    grid=True
)
plt.tight_layout()
plt.show()
