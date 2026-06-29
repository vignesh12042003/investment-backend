import uuid

from decimal import Decimal

from django.conf import settings
from django.db import models

from .asset import Asset
from .base import BaseModel
from .wallet import Wallet


class Transaction(BaseModel):
    """
    Stores every investment transaction.
    This is the source of truth for the portfolio.
    """

    class TransactionType(models.TextChoices):
        BUY = "BUY", "Buy"
        SELL = "SELL", "Sell"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        related_name="transactions"
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name="transactions"
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices
    )

    quantity = models.DecimalField(
        max_digits=18,
        decimal_places=4
    )

    price_per_unit = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    transaction_date = models.DateField()

    class Meta:
        ordering = ["-transaction_date", "-created_at"]

    def __str__(self):
        return (
            f"{self.transaction_type} | "
            f"{self.asset.symbol} | "
            f"{self.quantity}"
        )