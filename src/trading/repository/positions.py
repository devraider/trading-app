from django.db import transaction as db_transaction
from trading.models import DailyNetPosition
from trading.repository.base_repo import DF_VALUE, Repository


class DailyNetPositionRepo(Repository):
    def save_transactions(self, positions: list[dict[str, DF_VALUE]]) -> None:
        """Save multiple positions using bulk_create for efficiency.
        Args:
            positions: A list of dictionaries representing transaction data.

        Returns:
            None
        """
        transaction_objects = [
            DailyNetPosition(
                date=p["Date"],
                symbol=p["Symbol"],
                net_position=p["Net Position"],
            )
            for p in positions
        ]

        with db_transaction.atomic():
            DailyNetPosition.objects.bulk_create(transaction_objects)
