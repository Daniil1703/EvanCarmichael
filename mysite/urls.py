from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('polls.urls')),
    path('',include('users.urls')),
    path('',include('favorites.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('captcha/', include('captcha.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
