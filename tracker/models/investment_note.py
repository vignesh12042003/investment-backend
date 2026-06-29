import uuid

from django.conf import settings
from django.db import models

from .base import BaseModel
from .transaction import Transaction


class InvestmentNote(BaseModel):
    """
    Stores notes related to an investment transaction.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="investment_notes"
    )

    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    title = models.CharField(
        max_length=150
    )

    note = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title