import uuid

from decimal import Decimal

from django.conf import settings
from django.db import models

from .asset import Asset
from .base import BaseModel


class Holding(BaseModel):
    """
    Represents the user's current holding for an asset.
    This table is updated whenever a BUY or SELL transaction occurs.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="holdings"
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="holdings"
    )

    quantity = models.DecimalField(
        max_digits=18,
        decimal_places=4,
        default=Decimal("0.0000")
    )

    average_buy_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    invested_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    class Meta:
        ordering = ["asset__display_name"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "asset"],
                name="unique_user_asset_holding"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.asset.symbol}"