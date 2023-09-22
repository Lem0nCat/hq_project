from django.contrib import admin
from django.urls import path

from lessons.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/test/', AvailableLessonListAPIView.as_view()),
    path('api/v1/test2/', ProductViewSet.as_view({'get': 'list'})),
    path('api/v1/availablelessonslist/', CombinedDataView.as_view()),
    path('api/v1/availablelessonslist/<int:pk>/', CombinedDataView.as_view()),
]
