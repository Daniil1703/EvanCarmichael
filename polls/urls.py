from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.admin.views.decorators import staff_member_required
from . import views
# from .views import *

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.serchArticles, name='search_article'),
    path('post/create', 
          staff_member_required(views.PostCreate.as_view()), 
          name='post_create_url'),
    path('post/<str:slug>/', 
          views.PostDetail.as_view(),
          name="post_detail_url"),
    path('tags/', views.tags_list, name='tags_list'),
    path('tags/choise',
          staff_member_required(views.TagChoice.as_view()), 
          name='tag_choice_url'),
    path('tag/create', 
         staff_member_required(views.TagCreate.as_view()), 
         name='tag_create_url'),
    path('tag/<str:slug>/', views.TagDetail.as_view(), name='tag_detail'),
    path('tag/<str:slug>/update/', 
          staff_member_required(views.TagUpdate.as_view()), 
          name='tag_update_url'),
    path('tag/<str:slug>/delete', 
         staff_member_required(views.TagDelete.as_view()), 
         name='tag_delete_url'),
    path('post/<str:slug>/<str:pk>/remove/', 
          views.comment_remove, 
          name='comment_remove')
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)
