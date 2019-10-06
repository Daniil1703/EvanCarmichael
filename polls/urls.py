from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.loginUser, name='login'),
    path('register/', views.register, name="register"),
]