from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from time import time
from django.conf import settings
from users.models import CustomUser
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField
from django.template.defaultfilters import slugify as django_slugify
from django.utils.translation import gettext_lazy as _

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
            'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k',
            'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
            'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
            'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def gen_slug(s):
    return django_slugify(''.join(alphabet.get(w, w)\
                          for w in s.lower()) + '-' + str(int(time())))

class PageHit(models.Model):
    url = models.SlugField(max_length=150, blank=True, unique=True)
    count = models.PositiveIntegerField(default=0)

class Post(models.Model):
    class HowPublicate(models.TextChoices):
        LIST = 'L', _('Лента')
        BILBOARD = 'B', _('Слайдер')

    date_pub = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = RichTextUploadingField(blank=True)
    article_image = models.ImageField(
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
        verbose_name = _('статью')
        verbose_name_plural = _('статьи')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(_('Название категории'), max_length=50)
    slug = models.SlugField(_('URL'), max_length=50, blank=True, unique=True)
    tag_image = models.ImageField(_('Изображение'), 
                                  upload_to='categories/%Y/',
                                  blank = True,null = True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']
        verbose_name = _('категорию')
        verbose_name_plural = _('категории')

class Comment(models.Model):

    body = models.TextField(_('Комментарий'))
    created_time = models.DateTimeField(_('Дата добавления'), auto_now_add=True)
    last_mod_time = models.DateTimeField(_('Дата изменения'), auto_now=True)
    author = models.ForeignKey(
        CustomUser,
        verbose_name='author',
        on_delete=models.CASCADE)
    article = models.ForeignKey(
        Post,
        verbose_name='article',
        on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        'self',
        verbose_name="main_comment",
        blank=True,
        null=True,
        related_name='replies',
        on_delete=models.CASCADE)
    is_enable = models.BooleanField(
        _('Активен'), default=True, blank=False, null=False)

    class Meta:
        ordering = ['created_time']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        get_latest_by = 'id'

    def __str__(self):
        return self.body

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
