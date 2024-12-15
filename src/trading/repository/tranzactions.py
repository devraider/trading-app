from django.db import transaction as db_transaction
from trading.models import Transaction
from trading.repository.base_repo import DF_VALUE, Repository


class TransactionRepo(Repository):
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
