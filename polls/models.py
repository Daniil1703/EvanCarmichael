from django.db import models
from ckeditor.fields import RichTextField

class Post(models.Model):

    date_pub = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    body = RichTextField(blank=True, db_index=True)
    article_image = models.FileField(blank = True,null = True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    
    class Meta:
        ordering = ('-date_pub',)

    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)


    def __str__(self):
        return '{}'.format(self.title)