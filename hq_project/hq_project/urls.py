from django.contrib import admin
from django.urls import path, include

from lessons.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/availablelessonslist/', AvailableLessonListAPIView.as_view()),
]
