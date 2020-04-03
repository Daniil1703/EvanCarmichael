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

    # Система аунтентификации
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('account/', views.setting_account, name='account'),
    # path('account/password_change/',
    #          auth_views.PasswordChangeView.as_view(success_url=reverse_lazy(\
    #          'polls:password_change_done')), name='password_change'),
    # path('account/password_change/done/',
    #          auth_views.PasswordChangeDoneView.as_view(),
    #          name='password_change_done'),
    # path('login/password_reset/',
    #          auth_views.PasswordResetView.as_view(\
    #          success_url=reverse_lazy('polls:password_reset_done')),
    #          name='password_reset'),
    # path('login/password_reset/done',
    #          auth_views.PasswordResetDoneView.as_view(),
    #          name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',
    #          auth_views.PasswordResetConfirmView.as_view(\
    #          success_url=reverse_lazy('polls:password_reset_complete')),
    #          name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
    #          name='password_reset_complete'),
    # path('account/register/', views.register, name='register'),

]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
