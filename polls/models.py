from django.db import models


class Post(models.Model):

    date_pub = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    body = models.TextField(blank=True, db_index=True)
    article_image = models.FileField(blank = True,null = True)

    def __str__(self):
        return self.title
