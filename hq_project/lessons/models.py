from django.db import models

from embed_video.fields import EmbedVideoField

from django.contrib.auth.models import User


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    video_url = EmbedVideoField(null=True, blank=True)
    viewing_time = models.IntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
    

class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    time_watched = models.IntegerField()
    is_viewed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'
