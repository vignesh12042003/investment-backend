from rest_framework import serializers
from .models import Portfolio, Watchlist


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id', 'stock_symbol', 'total_quantity', 'avg_buy_price']


class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ['stock_symbol']

from .models import Transaction

from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "stock_symbol",
            "transaction_type",
            "quantity",
            "price",
            "created_at",
        ]
        read_only_fields = ["price", "created_at"]

def validate_quantity(self, value):
    if value <= 0:
        raise serializers.ValidationError("Quantity must be greater than 0")
    return value

