from functools import wraps
from django.db.models import F
from django.db import transaction
from .models import PageHit

def counted(f):
    @wraps(f)
    def decorator(request, slug, *args, **kwargs):
        with transaction.atomic():
            counter, created = PageHit.objects.get_or_create(url=slug)
            counter.count = F('count') + 1
            counter.save()
        return f(request, slug, *args, **kwargs)
    return decorator