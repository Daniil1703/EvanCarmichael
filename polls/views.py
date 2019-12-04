from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .forms import NewUserForm, LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Post, Tag, Profile
from .utils import ObjectDetailMixin


# ИСПОЛЬЗОВАНИЕ МЕТОДА CLASS BASED VIEWS
class PostDetail(ObjectDetailMixin, View):
        model = Post
        template = 'polls/post_detail.html'

class TagDetail(ObjectDetailMixin, View):
        model = Tag
        template = 'polls/tag_detail.html'



# Отображение постов
def index(request):
        posts = Post.objects.all()
        paginator = Paginator(posts, 9)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        is_paginated = page.has_other_pages()

        if page.has_next():
                next_url = '?page={}'.format(page.next_page_number())
        else:
                next_url = ''

        context = {
                'page_object': page,
                'is_paginated': is_paginated,
                'next_url': next_url
        }


        return render(request, 'polls/index.html', context=context)


def tags_list(request):
        tags = Tag.objects.all()
        return render(request, 'polls/tags_list.html', context={'tags': tags})

def Bookmark(request):
    return render(request, 'polls/bookmarks.html', context=None)

def setting_account(request):
    return render(request, 'registration/settings.html', context=None)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # СОЗДАЕМ НОВОГО пользователя
            new_user = user_form.save(commit=False)
            # ЗАДАЕМ ПОЛЬЗОВАТЕЛЮ ШИФРОВАННЫЙ ПАРОЛЬ
            new_user.set_password(user_form.cleaned_data['password'])
            # СОХРАНЯЕМ ВСЕ ДАННЫЕ В БД
            new_user.save()
            # Создание профиля пользователя
            Profile.objects.create(user=new_user)
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

@login_required
def setting_account(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'registration/settings.html', {'user_form': user_form,'profile_form': profile_form})
