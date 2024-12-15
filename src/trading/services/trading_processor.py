from io import BytesIO

import pandas as pd

from src.trading.repository.tranzactions import TransactionRepo


class TradingProcessor:
    """ """

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def calc_daily_net(self) -> pd.DataFrame:
        """Calculate daily net positions for each distinct Symbol.
        A "net position" is calculated as the product of the transaction quantity, price and a directional
        multiplier (positive for "BUY" and negative for "SELL"). The function then aggregates these positions at
        the level of "Date" and "Symbol" to provide a summary of net positions per day.
        Returns:
            A DataFrame containing the daily net positions with the columns:
            - `Date` (datetime): The date of the transaction.
            - `Symbol` (str): The identifier of the asset.
            - `Net Position` (float): The net position for the asset on the given date.
        """
        self._df["Net Position"] = self._df.apply(
            lambda row: row["Quantity"]
            * row["Price"]
            * (1 if row["Direction"] == "BUY" else -1),
            axis=1,
        )
        net_positions = (
            self._df.groupby(["Date", "Symbol"])
            .agg({"Net Position": "sum"})
            .reset_index()
        )
        return net_positions

    def save(self, repo: TransactionRepo):
        if self._df is None:
            raise ValueError("No transactions DataFrame to save.")
        transactions = self._df.to_dict(orient="records")
        repo.save_transactions(transactions)

    @property
    def df(self):
        return self._df

    @classmethod
    def from_excel(cls, file: BytesIO) -> "TradingProcessor":
        """
        Instantiate TradingProcessor class from an Excel file.
        Args:
            file: Bytes representation of an Excel file.

        Returns:
            Instance of TradingProcessor
        """
        return cls(pd.read_excel(file))
