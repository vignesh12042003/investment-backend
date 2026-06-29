import uuid

from decimal import Decimal

from django.conf import settings
from django.db import models

from .base import BaseModel


class Goal(BaseModel):
    """
    Represents an investment goal.
    """

    class GoalStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="goals"
    )

    title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    target_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    target_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=GoalStatus.choices,
        default=GoalStatus.ACTIVE
    )

    class Meta:
        ordering = ["target_date", "title"]

    def __str__(self):
        return self.title