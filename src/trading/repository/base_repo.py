from datetime import datetime
from typing import Protocol

import pandas as pd

DF_VALUE = datetime | int | float | str


class Repository(Protocol):
    """
    Interface for transaction storage and retrieval.
    Concrete implementations should interact with the database or other storage backends.
    """

    def save_transactions(self, transactions: list[dict[str, DF_VALUE]]) -> None:
        """
        Save multiple transactions.

        Args:
            transactions: A list of dictionaries representing transaction data.
        """
        ...

    def fetch_all_transactions(self) -> pd.DataFrame:
        """
        Fetch all transactions.

        Returns:
            A DataFrame containing all transactions.
        """
        ...
