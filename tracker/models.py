from django.db import models
from django.contrib.auth.models import User


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=20)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'stock_symbol')

    def __str__(self):
        return f"{self.user.username} - {self.stock_symbol}"


class Transaction(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'

    TRANSACTION_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=20)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_CHOICES)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.stock_symbol}"



class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=20)
    total_quantity = models.PositiveIntegerField()
    avg_buy_price = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'stock_symbol')

    def __str__(self):
        return f"{self.user.username} - {self.stock_symbol}"
