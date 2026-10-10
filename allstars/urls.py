from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # ---- The admin panel lives on its own, fully separate URL branch ----
    path('admin/', admin.site.urls),

    # ---- Public showcase ----
    path('', include('catalog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)