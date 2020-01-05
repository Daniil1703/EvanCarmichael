from django.shortcuts import render, redirect
from polls.models import Post
# Create your views here.

def favorites_list(request):
    posts = Post.objects.all()
    context = {
            'posts': posts
    }
    return render(request, 'favorites/favorites_list.html', context=context)

def add_to_favorites(request, id):
    if request.method == "POST":
        if not request.session.get('favorites'):
            request.session['favorites'] = list()
        else:
            request.session['favorites'] = list(request.session['favorites'])

        item_exist = next((item for item in request.session['favorites'] if
                            item['type'] == request.POST.get('type') and
                            item['id'] == id), False)

        add_data = {
            'type': request.POST.get('type'),
            'id': id,
        }

        if not item_exist:
            request.session['favorites'].append(add_data)
            request.session.modified = True
    return redirect(request.POST.get('url_from'))

def remove_from_favorites(request,id):
    if request.method == 'POST':
        for item in request.session['favorites']:
            if item['id'] == id and item['type'] == request.POST.get('type'):
                item.clear()

        while {} in request.session['favorites']:
            request.session['favorites'].remove({})

        if not request.session['favorites']:
            del request.session['favorites']

        request.session.modified = True
    return redirect(request.POST.get('url_from'))

def delete_favorites(request):
    if request.session.get('favorites'):
        del request.session['favorites']
    return redirect(request.POST.get('url_from'))

def favorites(request):
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


        return render(request, 'favorites/favorites_list.html', context=context)
