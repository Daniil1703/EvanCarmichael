from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator

from .forms import NewUserForm
from .models import Post, Tag
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
