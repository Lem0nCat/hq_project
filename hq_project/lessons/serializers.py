from rest_framework import serializers

from .models import *


class LessonViewSerializer(serializers.ModelSerializer):
    is_viewed = serializers.BooleanField(read_only=True)
    class Meta:
        model = LessonView
        fields = ['view_time', 'last_viewed_date', 'is_viewed']

class LessonSerializer(serializers.ModelSerializer):
    views = LessonViewSerializer(source='user_views', many=True, read_only=True)
    class Meta:
        model = Lesson
        fields = ['name', 'video_url', 'duration', 'views']

class CombinedDataSerializer(serializers.ModelSerializer):
    is_viewed = serializers.SerializerMethodField()
    view_time = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['name', 'video_url', 'duration', 'is_viewed', 'view_time']

    def get_is_viewed(self, obj):
        user_lesson = LessonView.objects.filter(user=self.context['request'].user, lesson=obj).first()
        return user_lesson.is_viewed if user_lesson else False

    def get_view_time(self, obj):
        user_lesson = LessonView.objects.filter(user=self.context['request'].user, lesson=obj).first()
        return user_lesson.view_time if user_lesson else 0

class RawDataSerializer(serializers.Serializer):
    name = serializers.CharField()
    video_url = serializers.URLField()
    view_time = serializers.IntegerField()
    is_viewed = serializers.CharField()

class UpdateRawDataSerializer(RawDataSerializer):
    last_viewed_date = serializers.DateField()

class LessonSerializerWithStatus(LessonSerializer):
    view_time = serializers.IntegerField(read_only=True)
    is_viewed = serializers.CharField(read_only=True)

    class Meta(LessonSerializer.Meta):
        fields = ['name', 'video_url', 'view_time', 'is_viewed']

    def to_representation(self, instance):
        user = self.context['request'].user
        data = super().to_representation(instance)
        status_and_duration = instance.get_status_and_duration(user)
        data.update(status_and_duration)
        return data
