from rest_framework import serializers
from tracker.models import Goal


class GoalSerializer(serializers.ModelSerializer):
    """
    Read Serializer
    """

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class GoalWriteSerializer(serializers.ModelSerializer):
    """
    Create / Update Serializer
    """

    class Meta:
        model = Goal
        fields = (
            "title",
            "description",
            "target_amount",
            "target_date",
            "status",
        )