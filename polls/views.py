from .forms import CommentForm, TagForm, PostForm
from .models import Post, Tag, Comment
from .utils import ObjectDetailMixin, ObjectUpdateMixin

from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from users.models import CustomUser

class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'polls/tag_detail.html'

class TagUpdate(ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'polls/tag_update.html'
    redirect_url = 'polls:tag_choice_url'

class TagDelete(View):
    def post(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        tag.delete()
        messages.success(request, 'Запись удалена!')
        return redirect('polls:tag_choice_url')

class TagCreate(View):
    def get(self, request):
        form = TagForm()
        return render(request, 'polls/tag_create.html', context={'form': form})

    def post(self, request):
        form = TagForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно опубликованы!')
            return redirect('polls:tags_list')
        else:
            messages.error(request, 'Упс... Такая категория уже есть!')
            return redirect('polls:tag_create_url')

class TagChoice(View):
    def get(self, request):
        tags = Tag.objects.all()
        return render(request, 'polls/tags_choice.html', context={'tags': tags})

class PostCreate(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'polls/post_create.html', context={'form': form})
    
    def post(self, request):
        bound_form = PostForm(request.POST, request.FILES)
        print(bound_form.is_valid())
        if bound_form.is_valid():
            bound_form.save()
            messages.success(request, 'Данные успешно опубликованы!')
            return redirect('polls:index')
        else:
            messages.error(request, 'Упс... Что-то пошло не так, проверьте\
                                     введеные данные и повторите попытку.')
            return render(request, 'polls/post_create.html', 
                          context={'form': bound_form})

class PostDetail(View):
    template_name = 'polls/post_detail.html'
    form_class = CommentForm()
    def get(self, request, slug):
        post = get_object_or_404(Post, slug__iexact=slug)
        comment = Comment.objects.all().filter(is_enable=True,
                                               parent_comment_id=None)
        context = {
            'post': post,
            'comment': comment,
            'form_class': self.form_class
        }
        return render(
            request, template_name=self.template_name, context=context)

    def post(self, request, slug):
        if request.method == 'POST':
            comment = Comment.objects.all().filter(is_enable=True,
                                                   parent_comment_id=None)
            form = CommentForm(request.POST)
            post = get_object_or_404(Post, slug__iexact=slug)
            if form.is_valid():
                perent = request.POST.get('comments_id')
                comments_qs = None
                if perent:
                    comments_qs = perent
                comment_to = Comment(
                    parent_comment_id = comments_qs,
                    article_id=post.id,
                    author_id=request.user.id,
                    body=form.cleaned_data['body'])
                comment_to.save()
        else:
            form = CommentForm()

        context = {
            'post': post,
            'comment': comment,
            'form_class': self.form_class
        }

        if request.is_ajax():
            html = render_to_string('polls/includes/comments.html',
                                    context, request=request)
            return JsonResponse({'forms': html})
        return render(
            request, template_name=self.template_name, context=context)


@login_required
def comment_remove(request, slug, pk):
    post = get_object_or_404(Post, slug__iexact=slug)
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.id == comment.author.id:
        comment.delete()
    else:
        raise Http404()

    return redirect('polls:post_detail_url', slug=post.slug)

# Отображение постов
def index(request):
    postsB = Post.objects.all().filter(publicate_in="B")



    posts = Post.objects.all().filter(publicate_in="L")
    paginator = Paginator(posts, 6)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'postsB': postsB,
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url
    }
    return render(request, 'polls/index.html', context=context)

def serchArticles(request):
    search_query = request.GET.get('search','')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) |
                                    Q(body__icontains=search_query))

        tags = Tag.objects.filter(Q(title__icontains=search_query))
        context = {
            'posts': posts,
            'tags': tags
        }
    else:
        context = None
    return render(request, 'polls/search_article.html', context=context)

def tags_list(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
    else:
        return redirect('polls:index')
    return render(request, 'polls/tags_list.html', context={'tags': tags})
