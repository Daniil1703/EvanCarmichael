from django.contrib import admin
from .models import Post, Tag, Comment
from django.urls import reverse
from django.utils.html import format_html

admin.site.register(Post)
admin.site.register(Tag)

def disable_commentstatus(modeladmin, request, queryset):
    queryset.update(is_enable=False)


def enable_commentstatus(modeladmin, request, queryset):
    queryset.update(is_enable=True)


disable_commentstatus.short_description = 'Отключить комментарии'
enable_commentstatus.short_description = 'Включить комментарии'

class CommentAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'id',
        'body',
        'link_to_userinfo',
        'link_to_article',
        'is_enable',
        'created_time')
    list_display_links = ('id', 'body')
    list_filter = ('author', 'article', 'is_enable')
    exclude = ('created_time', 'last_mod_time')
    actions = [disable_commentstatus, enable_commentstatus]

    def link_to_userinfo(self, obj):
        info = (obj.author._meta.app_label, obj.author._meta.model_name)
        link = reverse('admin:%s_%s_change' % info, args=(obj.author.id,))
        return format_html(
            u'<a href="%s">%s</a>' %
            (link, obj.author.login_user if obj.author.login_user else obj.author.email))

    def link_to_article(self, obj):
        info = (obj.author._meta.app_label, obj.author._meta.model_name)
        link = reverse('admin:%s_%s_change' % info, args=(obj.article.id,))
        return format_html(
            u'<a href="%s">%s</a>' % (link, obj.article.title))

    link_to_userinfo.short_description = 'Пользователь'
    link_to_article.short_description = 'Статья'

admin.site.register(Comment, CommentAdmin)
