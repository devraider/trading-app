from datetime import datetime
from typing import Protocol

import pandas as pd
from django.db import transaction as db_transaction
from trading.models import Transaction

DF_VALUE = datetime | int | float | str


class TransactionRepo(Protocol):
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


class PsqlTransactionRepo(TransactionRepo):
    def save_transactions(self, transactions: list[dict[str, DF_VALUE]]) -> None:
        """
        Save multiple transactions using bulk_create for efficiency.

        Args:
            transactions: A list of dictionaries representing transaction data.
        """
        transaction_objects = [
            Transaction(
                date=t["Date"],
                symbol=t["Symbol"],
                quantity=t["Quantity"],
                price=t["Price"],
                direction=t["Direction"],
            )
            for t in transactions
        ]

        with db_transaction.atomic():
            Transaction.objects.bulk_create(transaction_objects)
