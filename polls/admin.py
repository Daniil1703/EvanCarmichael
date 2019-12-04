from django.contrib import admin
from .models import Post, Tag, Profile

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Profile)

# @admin.register(Profile)
# class ProfileAdmin(Profile):
#     list_display = ['user','photo']
