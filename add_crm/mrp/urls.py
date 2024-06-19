from django.contrib import admin
from django.urls import include, path

from .views import *

urlpatterns = [
    path('', warehouse, name='warehouse'),
    path('purchase/', purchase, name='purchase'),
    path('take/', take, name='take'),
    path('application/<int:num>', application, name='application'),
    path('add_application/', add_application, name='add_application'),
    path('add_application_ts/', add_application_ts, name='add_application_ts'),
]