from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<str:slug>/', views.PostDetail.as_view(), name="post_detail_url"),
    path('tags/', views.tags_list, name='tags_list'),
    path('tag/<str:slug>/', views.TagDetail.as_view(), name='tag_detail'),
    path('bookmark/', views.Bookmark, name='bookmarks')

]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
