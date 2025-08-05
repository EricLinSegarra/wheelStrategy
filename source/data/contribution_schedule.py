import pandas as pd


def generate_contributions(start_date: str,
                           end_date: str,
                           monthly_amount: float = 500,
                           mode: str = "dca",        # "dca" | "lump_sum"
                           lump_sum_amount: float = 0,
                           lump_sum_date: str | None = None) -> pd.Series:
    """
    Generate calendar with  contributions.
    - DCA: monthly contributions at the end of the month or labor day (BME)
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
    - lump_sum: unique contribution in one specific date
    """
    if mode.lower() == "dca":
        dates = pd.date_range(start=start_date, end=end_date, freq="BME")
        s = pd.Series(monthly_amount, index=dates, name="cash_in")
        return s

    elif mode.lower() == "lump_sum":
        when = pd.Timestamp(lump_sum_date or start_date)
        return pd.Series(lump_sum_amount, index=[when], name="cash_in")

    else:
        raise ValueError("mode must be 'dca' or 'lump_sum'")


if __name__ == "__main__":
    contributions_test = generate_contributions('2010-01-01', '2024-12-31', 1000, 'dca', 50000, '2020-01-01')
    print(contributions_test)
