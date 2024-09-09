from django.contrib import admin
from django.urls import include, path

from .views import *

urlpatterns = [
    path('', warehouse, name='warehouse'),
    path('purchase/<str:link>', purchase, name='purchase'),
    path('take/', take, name='take'),
    path('application/<int:num>', application, name='application'),
    path('add_application/<str:link>', add_application, name='add_application'),
    path('add_application_ts/<str:link>', add_application_ts, name='add_application_ts'),
    path('add_equipment/<str:link>', add_equipment, name='add_equipment'),
    path('equipment/<int:num>', equipment, name='equipment'),
    path('technical_specification/<int:pk>', download_file, name='technical_specification'),
    path('technical_specification_upd/<int:num>', techical_specification, name='technical_specification_upd'),
    path('application/<int:num>', application, name='application'),
    path('csv/', update_warehouse_csv, name="csv"),
    path('gen_path/', gen_path, name="gen_path"),
]

urlpatterns.extend(urlpatterns_views)