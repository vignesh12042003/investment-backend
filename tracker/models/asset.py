import uuid

from django.db import models

from .base import BaseModel


class Asset(BaseModel):
    """
    Master table for all tradable assets.
    """

    class AssetType(models.TextChoices):
        STOCK = "STOCK", "Stock"
        ETF = "ETF", "ETF"

    class Exchange(models.TextChoices):
        NSE = "NSE", "National Stock Exchange"
        BSE = "BSE", "Bombay Stock Exchange"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    symbol = models.CharField(
        max_length=20,
        unique=True,
        db_index=True
    )

    display_name = models.CharField(
        max_length=150
    )

    asset_type = models.CharField(
        max_length=10,
        choices=AssetType.choices
    )

    exchange = models.CharField(
        max_length=10,
        choices=Exchange.choices
    )

    sector = models.CharField(
        max_length=100,
        blank=True
    )

    currency = models.CharField(
        max_length=10,
        default="INR"
    )

    isin = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["display_name"]
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

    def __str__(self):
        return f"{self.display_name} ({self.symbol})"