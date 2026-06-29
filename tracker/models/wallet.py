import uuid

from decimal import Decimal

from django.conf import settings
from django.db import models

from .base import BaseModel


class Wallet(BaseModel):
    """
    Represents a user's investment wallet.
    """

    class WalletType(models.TextChoices):
        BANK = "BANK", "Bank Account"
        BROKER = "BROKER", "Broker Account"
        CASH = "CASH", "Cash"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallets"
    )

    wallet_name = models.CharField(
        max_length=100
    )

    wallet_type = models.CharField(
        max_length=20,
        choices=WalletType.choices,
        default=WalletType.BANK
    )

    current_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["wallet_name"]
        unique_together = ("user", "wallet_name")

    def __str__(self):
        return f"{self.wallet_name} ({self.user.username})"