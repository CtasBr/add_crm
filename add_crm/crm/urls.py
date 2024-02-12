from django.urls import include, path

from .views import *

urlpatterns = [
    path('', main, name='main'),
]