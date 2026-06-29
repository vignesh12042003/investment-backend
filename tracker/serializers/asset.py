from rest_framework import serializers
from tracker.models import Asset


class AssetSerializer(serializers.ModelSerializer):
    """
    Read Serializer
    Used for GET APIs
    """

    class Meta:
        model = Asset
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class AssetWriteSerializer(serializers.ModelSerializer):
    """
    Create / Update Serializer
    Used for POST, PUT and PATCH APIs
    """

    class Meta:
        model = Asset
        fields = (
            "symbol",
            "display_name",
            "asset_type",
            "exchange",
            "sector",
            "currency",
            "isin",
            "is_active",
        )