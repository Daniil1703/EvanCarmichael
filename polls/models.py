from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from time import time

def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))



class Post(models.Model):

    date_pub = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = RichTextField(blank=True, db_index=True)
    article_image = models.FileField(blank = True,null = True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    title_detail = RichTextField(blank=True, db_index=True)

    class Meta:
        ordering = ('-date_pub',)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, unique=True)
    tag_image = models.FileField(blank = True,null = True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.title)
