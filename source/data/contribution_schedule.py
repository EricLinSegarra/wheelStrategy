import pandas as pd


def generate_contributions(start_date: str, end_date: str, monthly_amount: float = 500) -> pd.Series:
    """
    Generates a monthly contribution schedule.

    Parameters:
        start_date (str): Starting date (format 'YYYY-MM-DD')
        end_date (str): Ending date (format 'YYYY-MM-DD')
        monthly_amount (float): Amount contributed each month

    Returns:
        pd.Series: Date-indexed monthly contributions
    """
    dates = pd.date_range(start=start_date, end=end_date, freq='ME')
    contributions = pd.Series(monthly_amount, index=dates, name="cash_in")
    return contributions
