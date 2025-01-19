from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web_portal.urls')),
    path('web_portal/', include('web_portal.urls')),
]
