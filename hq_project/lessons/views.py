from django.db import connection, reset_queries
from django.db.models import Count, OuterRef, Subquery, Sum
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


class CombinedDataView(APIView):
    def calculate_viewed_status(self, view_time, duration):
        return 'yes' if (view_time >= 0.8 * duration) else 'no'

    def get(self, request, pk=None):
        reset_queries()
        sql_query = f"""SELECT ls.id, ls.name, ls.video_url, 
                        ls.duration, lsview.view_time, lsview.last_viewed_date
                        FROM lessons_lesson ls, lessons_product_lessons pr_ls, lessons_product pr, lessons_access acs
                        LEFT OUTER JOIN lessons_lessonview lsview ON lsview.user_id = %s AND
                        lsview.lesson_id = ls.id
                        WHERE ls.id = pr_ls.lesson_id AND
                        pr_ls.product_id = pr.id AND
                        pr.id = acs.product_id AND
                        acs.user_id = %s"""
        if (not pk):
            lessons = Lesson.objects.raw(
                sql_query, [request.user.id, request.user.id])
        else:
            sql_query += 'AND ls.id = %s'
            lessons = Lesson.objects.raw(
                sql_query, [request.user.id, request.user.id, pk])

        for lesson in lessons:
            if (lesson.view_time == None):
                lesson.view_time = 0
            lesson.is_viewed = self.calculate_viewed_status(
                lesson.view_time, lesson.duration)
        if (not pk):
            response = Response(
                {'lessons': RawDataSerializer(lessons, many=True).data})
        else:
            response = Response(
                {'lessons': UpdateRawDataSerializer(lessons, many=True).data})

        print(f'SQL ЗАПРОСОВ -> {len(connection.queries)}')
        return response


class ProductStatisticsView(APIView):
    def get(self, request):
        reset_queries()
        subscribers_count_subquery = Product.objects.filter(id=OuterRef('id')
                                                            ).annotate(number_of_users_on_product=Count('users')
                                                                       ).values('number_of_users_on_product')

        #   2 SQL запроса
        products = Product.objects.annotate(
            lessons_viewed_count=Count('lessons__lessonview'),
            total_time_spent_by_users=Sum('lessons__lessonview__view_time'),
            number_of_users_on_product=Subquery(subscribers_count_subquery),
            product_purchase_percentage=Subquery(
                subscribers_count_subquery) * 100 / User.objects.count()
        ).values('id', 'name',
                 'lessons_viewed_count',
                 'total_time_spent_by_users',
                 'number_of_users_on_product',
                 'product_purchase_percentage')

        #   1 SQL запрос
        # products = Product.objects.raw("""SELECT pr.id, pr.name,
        #                                COUNT(lsview.id) AS lessons_viewed_count,
        #                                SUM(lsview.view_time) AS total_time_spent_by_users,
        #                                (SELECT COUNT(*) FROM lessons_product in_pr, lessons_access acs, auth_user usr
        #                                WHERE in_pr.id = acs.product_id AND acs.user_id = usr.id AND in_pr.id = pr.id) AS number_of_users_on_product,
        #                                ((SELECT COUNT(*) FROM lessons_product in_pr, lessons_access acs, auth_user usr
        #                                WHERE in_pr.id = acs.product_id AND acs.user_id = usr.id AND in_pr.id = pr.id) * 100 / (SELECT COUNT(*) FROM auth_user)) AS product_purchase_percentage
        #                                FROM lessons_product pr, lessons_lesson ls, lessons_product_lessons pr_ls, lessons_lessonview lsview
        #                                WHERE pr.id = pr_ls.product_id AND
        #                                pr_ls.lesson_id = ls.id AND
        #                                ls.id = lsview.lesson_id GROUP BY pr.id""")

        response = Response(
            {'products': ProductStatisticsSerializer(products, many=True).data})
        print(f'SQL ЗАПРОСОВ -> {len(connection.queries)}')
        return response
