from io import BytesIO

import pandas as pd


class TradingProcessor:
    """ """

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def calc_daily_net(self):
        pass

    def save(self):
        pass

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
