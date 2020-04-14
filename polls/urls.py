from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
# from .views import *

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.serchArticles, name='search_article'),
    path('post/<str:slug>/', views.PostDetail.as_view(), name="post_detail_url"),
    path('tags/', views.tags_list, name='tags_list'),
    path('tag/<str:slug>/', views.TagDetail.as_view(), name='tag_detail'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
