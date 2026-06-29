from rest_framework import serializers
from tracker.models import Watchlist


class WatchlistSerializer(serializers.ModelSerializer):
    """
    Read Serializer
    """

    asset_symbol = serializers.CharField(
        source="asset.symbol",
        read_only=True
    )

    asset_name = serializers.CharField(
        source="asset.display_name",
        read_only=True
    )

    class Meta:
        model = Watchlist
        fields = (
            "id",
            "asset",
            "asset_symbol",
            "asset_name",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class WatchlistWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Watchlist
        fields = (
            "asset",
        )