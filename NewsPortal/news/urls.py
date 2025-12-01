from django.urls import path
from .views import *


urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('news/<int:pk>', PostDetail.as_view(), name='news_detail'),
   path('articles/<int:pk>', PostDetail.as_view(), name='articles_detail'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
   path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
]