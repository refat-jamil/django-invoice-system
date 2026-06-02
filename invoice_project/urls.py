from django.contrib import admin
from django.urls import path, include  # ← add include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('invoices/', include('invoices.urls')),  # ← add this
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)