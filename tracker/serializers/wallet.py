from rest_framework import serializers
from tracker.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """
    Read Serializer
    """

    class Meta:
        model = Wallet
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class WalletWriteSerializer(serializers.ModelSerializer):
    """
    Create / Update Serializer
    """

    class Meta:
        model = Wallet
        fields = (
            "wallet_name",
            "wallet_type",
            "is_active",
        )

    def validate_wallet_name(self, value):
        return value.strip()