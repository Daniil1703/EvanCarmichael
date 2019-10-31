from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm


# Create your views here.

def index(request):
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return render(request, 'polls/index.html',  {'posts': posts})


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