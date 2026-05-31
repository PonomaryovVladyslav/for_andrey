# blog/urls.py
from django.urls import path

from blog import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='home'),
    path('my-feed/', views.MyFeedView.as_view(), name='my-feed'),

    path('create/', views.ArticleCreateView.as_view(), name='article-create'),

    path('topics/', views.TopicListView.as_view(), name='topic-list'),
    path('topics/<int:topic_id>/', views.TopicDetailView.as_view(), name='topic-detail'),
    path('topics/<int:topic_id>/subscribe/', views.TopicSubscribeView.as_view(), name='topic-subscribe'),
    path('topics/<int:topic_id>/unsubscribe/', views.TopicUnsubscribeView.as_view(), name='topic-unsubscribe'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('set-password/', views.SetPasswordView.as_view(), name='set-password'),
    path('login/', views.BlogLoginView.as_view(), name='login'),
    path('logout/', views.BlogLogoutView.as_view(), name='logout'),

    path('<int:year>/<int:month>/', views.ArticlesByMonthView.as_view(), name='articles-by-month'),

    path('<int:article_id>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('<int:article_id>/comment/', views.CommentCreateView.as_view(), name='article-comment'),
    path('<int:article_id>/update/', views.ArticleUpdateView.as_view(), name='article-update'),
    path('<int:article_id>/delete/', views.ArticleDeleteView.as_view(), name='article-delete'),
]

