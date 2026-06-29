from rest_framework import serializers
from tracker.models import Holding


class HoldingSerializer(serializers.ModelSerializer):
    """
    Holding is calculated automatically from Transactions.
    It is a Read Only Serializer.
    """

    asset_symbol = serializers.CharField(
        source="asset.symbol",
        read_only=True,
    )

    asset_name = serializers.CharField(
        source="asset.display_name",
        read_only=True,
    )

    class Meta:
        model = Holding
        fields = (
            "id",
            "asset",
            "asset_symbol",
            "asset_name",
            "quantity",
            "average_buy_price",
            "invested_amount",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields