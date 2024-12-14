from django.db import models


class Trade(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    symbol = models.CharField(max_length=10, db_index=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    direction = models.CharField(
        max_length=4, choices=[("BUY", "Buy"), ("SELL", "Sell")]
    )

    def __str__(self):
        return f"{self.date} - {self.symbol} - {self.direction} - {self.quantity} @ {self.price}"


class Position(models.Model):
    date = models.DateField()
    symbol = models.CharField(max_length=10)
    net_position = models.FloatField()

    def __str__(self):
        return f"{self.date} - {self.symbol} - Net Position: {self.net_position}"
