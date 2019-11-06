from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .forms import NewUserForm
from .models import Post, Tag
from .utils import ObjectDetailMixin
from .forms import TagForm


# ИСПОЛЬЗОВАНИЕ МЕТОДА CLASS BASED VIEWS
class PostDetail(ObjectDetailMixin, View):
        model = Post
        template = 'polls/post_detail.html'
   
class TagDetail(ObjectDetailMixin, View):
        model = Tag
        template = 'polls/tag_detail.html'

class TagCreate(View):
        def get(self, request):
                form = TagForm()
                return render(request, 'polls/includes/tag_create.html', context={'form': form})

        def post(self, request):
                bound_form = TagForm(request.POST)

                if bound_form.is_valid():
                        new_tag = bound_form.save()
                        return redirect('polls:tags_list')
                return render(request, 'polls/includes/tag_create.html', context={'form': bound_form})


# Отображение постов
def index(request):
        posts = Post.objects.all()
        return render(request, 'polls/index.html', {'posts': posts})


def tags_list(request):
        tags = Tag.objects.all()
        return render(request, 'polls/tags_list.html', context={'tags': tags})

def login_request(request):
        if request.method == 'POST':
                form = AuthenticationForm(request=request, data=request.POST)
                if form.is_valid():
                        username = form.cleaned_data.get('username')
                        password = form.cleaned_data.get('password')
                        user = authenticate(username=username, password=password)
                        if user is not None:
                                login(request, user)
                                messages.info(request, f"Вы авторизовались как {username}")
                                return redirect('polls:index')
                        else:
                                messages.error(request, f"NE")
                else:
                        messages.success(request, "К сожалению, вы ввели неверный пароль или логин. Проверьте данные еще раз.")

        form = AuthenticationForm()
        return render(request = request,template_name = "polls/login.html",context={"form":form})


def register(request):
        if request.method == "POST":
                form = UserCreationForm(request.POST)
                if form.is_valid():
                        user = form.save()
                        username = form.cleaned_data.get('username')
                        messages.success(request, f"Создан новый аккаунт: {username}")
                        login(request, user)
                        
                        return redirect('polls:index')
                else:
                        for msg in form.error_messages:
                                messages.error(request, f"{msg}: {form.error_messages[msg]}")

                        return render(request = request,template_name = "polls/register.html",context={"form":form})
        form = UserCreationForm
        return render(request = request, template_name = "polls/register.html",context={"form":form})

def logout_request(request):
        logout(request)
        messages.info(request, f"Вы вышли из системы!")
        return redirect("polls:index")