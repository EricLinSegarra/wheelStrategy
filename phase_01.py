# scripts/phase1.py
import argparse, pandas as pd, matplotlib.pyplot as plt, os
from source.data.contribution_schedule import generate_contributions
from source.engine.buy_and_hold import buy_and_hold_strategy
from source.engine.metrics import cagr, max_drawdown, annual_vol, sharpe


def run(ticker, start, end, mode, monthly, initial, lump_sum):
    data_path = f"data/{ticker}_daily.parquet"
    df_price = pd.read_parquet(data_path).loc[start:end]
    contrib = generate_contributions(
        start, end,
        monthly_amount=monthly,
        mode=mode,
        lump_sum_amount=lump_sum,
        lump_sum_date=start
    )
    df = buy_and_hold_strategy(df_price, contrib, initial_capital=initial)
    os.makedirs("outputs/phase1", exist_ok=True)
    out_csv = f"outputs/phase1/{ticker}_{mode}.csv"
    df.to_csv(out_csv, index=False)

    # métricas
    series = df.set_index("date")["capital"]
    print(f"\nResultados {ticker} ({mode}):")
    print(f"- CAGR: {cagr(series):.2%}")
    print(f"- Vol anual: {annual_vol(series):.2%}")
    print(f"- Max Drawdown: {max_drawdown(series):.2%}")
    print(f"- Sharpe (rf=0): {sharpe(series):.2f}")
    # plot
    series.plot(figsize=(11,5), title=f"{ticker} – {mode.upper()} Capital")
    plt.ylabel("USD"); plt.grid(True); plt.tight_layout(); plt.show()
    print(f"CSV guardado en: {out_csv}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ticker", default="SPY")
    p.add_argument("--start", required=True)        # ej: 2010-01-01
    p.add_argument("--end", required=True)          # ej: 2024-12-31
    p.add_argument("--mode", choices=["dca","lump_sum"], default="dca")
    p.add_argument("--monthly", type=float, default=500)
    p.add_argument("--initial", type=float, default=5000)
    p.add_argument("--lump_sum", type=float, default=0)
    args = p.parse_args()
    run(**vars(args))
