from django.http import HttpResponse
from django.urls import path

def simple_test(request):
    return HttpResponse("HOLA DESDE TEST - FUNCIONA!")

urlpatterns = [
    path('', simple_test, name='simple_test'),
]