from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *



class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template,
                      context={self.model.__name__.lower(): obj})

class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        context = {
            self.model.__name__.lower(): obj,
            'form': bound_form
        }
        return render(request, self.template, context=context)
    
    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)
        if bound_form.is_valid():
            bound_form.save()
            messages.success(request, 'Данные обновлены!')
            return redirect(self.redirect_url)
        else:
            messages.error(request, 'Упс... Такая запись уже есть!')
            return redirect(self.redirect_url)