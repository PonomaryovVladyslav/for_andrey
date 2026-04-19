# blog/urls.py
from django.urls import path, re_path
from blog.views import article_list, article_detail, articles_by_date

urlpatterns = [
    path('', article_list, name='article-list'),
    path('<int:pk>/', article_detail, name='article-detail'),
    # path('<slug:slug>/', article_by_slug, name='article-by-slug'),
    re_path(
        r'^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$',
        articles_by_date,
        name='articles-by-date'
    ),
]

