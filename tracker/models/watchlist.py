import uuid

from django.conf import settings
from django.db import models

from .asset import Asset
from .base import BaseModel


class Watchlist(BaseModel):
    """
    Stores assets the user wants to monitor.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watchlists"
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="watchlists"
    )

    class Meta:
        ordering = ["asset__display_name"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "asset"],
                name="unique_watchlist_asset"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.asset.symbol}"