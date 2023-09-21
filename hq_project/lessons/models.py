from django.db import models

from embed_video.fields import EmbedVideoField

from django.contrib.auth.models import User


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    video_url = EmbedVideoField(null=True, blank=True)
    viewing_time = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
    def get_status_and_duration(self, user):
        try:
            lesson_view = LessonView.objects.get(user=user, lesson=self)
            time_watched = lesson_view.time_watched
            is_viewed = "No"
        except LessonView.DoesNotExist:
            time_watched = 0
            is_viewed = "No"

        if time_watched >= (0.8 * self.viewing_time):
            is_viewed = "Yes"

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
    time_watched = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user} - {self.lesson}'

    class Meta:
        verbose_name = 'Просмотр урока'
        verbose_name_plural = 'Просмотры уроков'


class Product(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_products')
    lessons = models.ManyToManyField(Lesson)
    users = models.ManyToManyField(User, through="Access", related_name='products')

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
