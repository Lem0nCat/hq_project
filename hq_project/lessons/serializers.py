from rest_framework import serializers

from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = '__all__'

class LessonSerializerWithStatus(LessonSerializer):
    time_watched = serializers.IntegerField(read_only=True)
    is_viewed = serializers.CharField(read_only=True)

    class Meta(LessonSerializer.Meta):
        fields = '__all__'

    def to_representation(self, instance):
        user = self.context['request'].user
        data = super().to_representation(instance)
        status_and_duration = instance.get_status_and_duration(user)
        data.update(status_and_duration)
        return data
