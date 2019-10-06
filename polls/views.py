from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.

def index(request):
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return render(request, 'polls/index.html',  {'posts': posts})

def loginUser(request):
    return render(request, 'polls/login.html',)

def register(request):
        if request.method == "POST":
                form = UserCreationForm(request.POST)
                if form.is_valid():
                        user = form.save()
                        username = form.cleaned_data.get('username')
                        user.save()
                        login(request,user)
                        return redirect('polls:index')
                else:
                        for msg in form.error_messages:
                                print(form.error_messages[msg])

                        return render(request = request,template_name = "polls/register.html",context={"form":form})
        form = UserCreationForm
        return render(request = request,
                template_name = "polls/register.html",context={"form":form})