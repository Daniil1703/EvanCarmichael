from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import PassChForm, PassResForm, SetPassForm
from .views import *

app_name = 'users'


urlpatterns = [
    path('registration/', UserCreate.as_view(), name='user_create_url'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    path('password_change/',
        auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html',
        success_url=reverse_lazy('users:password_change_done'),
        form_class=PassChForm
        ),
        name='password_change'),

    path('', message_change_password, name='password_change_done'),

    path('password_reset',
        auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html',
        success_url='password_reset/done/',
        from_email='support@yoursite.ma',
        subject_template_name='users/password_reset_subject.txt',
        form_class=PassResForm
        ),
        name='password_reset'),

    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete'),
        form_class=SetPassForm
        ),
        name='password_reset_confirm'),
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete')
]
