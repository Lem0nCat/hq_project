from django.db import models

from django.contrib.auth.models import User
from lessons.models import Lesson

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lessons = models.ManyToManyField(Lesson)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    

# class ProductLesson(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = 'Продукт-Урок'
#         verbose_name_plural = 'Продукты-Уроки'


class Access(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 

    class Meta:
        verbose_name = 'Доступ'
        verbose_name_plural = 'Доступы'
