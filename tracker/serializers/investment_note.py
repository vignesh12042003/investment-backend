from rest_framework import serializers
from tracker.models import InvestmentNote


class InvestmentNoteSerializer(serializers.ModelSerializer):
    """
    Read Serializer
    """

    asset_symbol = serializers.CharField(
        source="transaction.asset.symbol",
        read_only=True
    )

    transaction_type = serializers.CharField(
        source="transaction.transaction_type",
        read_only=True
    )

    class Meta:
        model = InvestmentNote
        fields = (
            "id",
            "transaction",
            "asset_symbol",
            "transaction_type",
            "title",
            "note",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class InvestmentNoteWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentNote
        fields = (
            "transaction",
            "title",
            "note",
        )