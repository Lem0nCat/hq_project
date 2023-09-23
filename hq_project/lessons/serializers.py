from rest_framework import serializers

from .models import *


class RawDataSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    video_url = serializers.URLField(read_only=True)
    view_time = serializers.IntegerField(read_only=True)
    is_viewed = serializers.CharField(read_only=True)


class UpdateRawDataSerializer(RawDataSerializer):
    last_viewed_date = serializers.DateField(read_only=True)


class ProductStatisticsSerializer(serializers.Serializer):
    name = serializers.CharField()
    lessons_viewed_count = serializers.IntegerField(read_only=True)
    total_time_spent_by_users = serializers.IntegerField(read_only=True)
    number_of_users_on_product = serializers.IntegerField(read_only=True)
    product_purchase_percentage = serializers.IntegerField(
        read_only=True, max_value=100)
