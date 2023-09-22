from django.db import models

from embed_video.fields import EmbedVideoField

from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_authors')
    lessons = models.ManyToManyField("Lesson")
    users = models.ManyToManyField(User, through="Access", related_name='allowed_users')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Access(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 

    def __str__(self):
        return f'{self.user} - {self.product}'

    class Meta:
        verbose_name = 'Доступ'
        verbose_name_plural = 'Доступы'

class Lesson(models.Model):
    name = models.CharField(max_length=255)
    video_url = models.URLField()
    duration = models.PositiveIntegerField()
    views = models.ManyToManyField(User, through="LessonView")

    def __str__(self):
        return self.name
    
    def get_status_and_duration(self, user):
        try:
            lesson_view = LessonView.objects.get(user=user, lesson=self)
            time_watched = lesson_view.view_time
            is_viewed = lesson_view.is_viewed
        except LessonView.DoesNotExist:
            time_watched = 0
            is_viewed = False

        return {
            "is_viewed": is_viewed,
            "time_watched": time_watched,
        }


    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    view_time = models.PositiveIntegerField(default=0)
    # is_viewed = models.BooleanField(default=False)
    last_viewed_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.lesson} - {self.last_viewed_date}'
    
    @property
    def is_viewed(self):
        return self.view_time >= 0.8 * self.lesson.duration

    class Meta:
        verbose_name = 'Просмотр урока'
        verbose_name_plural = 'Просмотры уроков'
