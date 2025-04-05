from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

def redirect_to_api(request):
    return HttpResponseRedirect('api/')  # Remove leading slash

urlpatterns = [
    path('', redirect_to_api, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include('compiler.urls')),
]
