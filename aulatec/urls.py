"""
URL configuration for aulatec project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def test_direct_view(request):
    return HttpResponse('¡Ruta directa funcionando!')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test-direct/', test_direct_view),
    path('', include('gestion_aulatec.urls')),  # Include the URLs from your app
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
=======


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion_aulatec.urls')),  # Include the URLs from your app
]
>>>>>>> 4e2f81b62d3d85f4ea86504f7061355e11f3faf0
