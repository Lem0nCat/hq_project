from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from django.db import reset_queries
from django.db.models import Prefetch

from .models import *
from .serializers import *
    

class AvailableLessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        available_products = Product.objects.filter(users=user)
        lessons = Lesson.objects.filter(product__in=available_products)
        print(connection.queries)
        return lessons

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return LessonSerializerWithStatus(*args, **kwargs)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        lesson_queryset = Lesson.objects.filter(product__users=self.request.user).prefetch_related(
            Prefetch('views', queryset=LessonView.objects.filter(user=self.request.user), to_attr='user_views')
        )
        return lesson_queryset


class CombinedDataView(APIView):
    def calculate_viewed_status(self, view_time, duration):
        return 'yes' if (view_time >= 0.8 * duration) else 'no'

    def get(self, request, pk=None):
        reset_queries()
        sql_query = f"""SELECT lessons_lesson.id, lessons_lesson.name, lessons_lesson.video_url, 
                        lessons_lesson.duration, lessons_lessonview.view_time, lessons_lessonview.last_viewed_date
                        FROM lessons_lesson, lessons_product_lessons, lessons_product, lessons_access
                        LEFT OUTER JOIN lessons_lessonview ON lessons_lessonview.user_id = 1 AND
                        lessons_lessonview.lesson_id = lessons_lesson.id
                        WHERE lessons_lesson.id = lessons_product_lessons.lesson_id AND
                        lessons_product_lessons.product_id = lessons_product.id AND
                        lessons_product.id = lessons_access.product_id AND
                        lessons_access.user_id = %s"""
        if(not pk):
            lessons = Lesson.objects.raw(sql_query, [request.user.id])
        else:
            sql_query += 'AND lessons_product.id = %s'
            lessons = Lesson.objects.raw(sql_query, [request.user.id, pk])
        
        for lesson in lessons:
            if (lesson.view_time == None): lesson.view_time = 0
            lesson.is_viewed = self.calculate_viewed_status(lesson.view_time, lesson.duration)
        if (pk):
            response = Response({'lessons': UpdateRawDataSerializer(lessons, many=True).data})
        else:
            response = Response({'lessons': RawDataSerializer(lessons, many=True).data})
        
        print(connection.queries)

        return response
