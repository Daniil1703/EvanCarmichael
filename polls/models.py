from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from time import time
from django.conf import settings
from django.template.defaultfilters import slugify as django_slugify
from django.utils.translation import gettext_lazy as _

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
            'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k',
            'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
            'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
            'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def gen_slug(s):
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()) + '-' + str(int(time())))



class Post(models.Model):

    class HowPublicate(models.TextChoices):
        LIST = 'L', _('Лента')
        BILBOARD = 'B', _('Слайдер')

    date_pub = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = RichTextUploadingField(blank=True)
    article_image = models.FileField(
        upload_to='posts/%Y/',
        blank = True,
        null = True
        )
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    publicate_in = models.CharField(
        _('Тип публикации:'),
        max_length=2,
        choices=HowPublicate.choices,
        default=HowPublicate.LIST,
        )

    class Meta:
        ordering = ['-date_pub']

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, unique=True)
    tag_image = models.FileField(upload_to='categories/%Y/', blank = True,null = True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']
