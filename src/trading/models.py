from django.db import models


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    symbol = models.CharField(max_length=10, db_index=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    direction = models.CharField(
        max_length=4, choices=[("BUY", "Buy"), ("SELL", "Sell")]
    )

    class Meta:
        db_table = "trading_transactions"
        indexes = [
            models.Index(fields=["symbol"]),
            models.Index(fields=["symbol", "date"]),
        ]

    def __str__(self):
        return f"{self.date} - {self.symbol} - {self.direction} - {self.quantity} @ {self.price}"


class DailyNetPosition(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=10, db_index=True)
    net_position = models.FloatField()
    date = models.DateField()

    class Meta:
        db_table = "trading_daily_net_positions"
        indexes = [
            models.Index(fields=["symbol"]),
            models.Index(fields=["symbol", "date"]),
        ]

    def __str__(self):
        return f"{self.date} - {self.symbol}  @  {self.net_position}"
