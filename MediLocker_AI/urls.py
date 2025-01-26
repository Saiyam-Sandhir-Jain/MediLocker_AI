from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = 'MediLocker_AI.urls.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web_portal.urls')),
    path('web_portal/', include('web_portal.urls')),
    path('report_reader/', include('report_reader.urls')),
]
