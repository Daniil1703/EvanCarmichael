from django import template
from polls.models import PageHit

register = template.Library()

@register.simple_tag(takes_context=True)
def page_hits(context, page_url=None):
    slug = context['request'].path
    slug = slug.replace('/post/','').replace('/', '')
    counter = (PageHit.objects
                      .filter(url=(slug if page_url is None else page_url))
                      .first())
    return 0 if counter is None else counter.count