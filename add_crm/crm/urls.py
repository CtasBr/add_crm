from django.urls import include, path

from .views import *

urlpatterns = [
    path('', projects, name='projects'),
    path('experiments/<int:id>', experiments, name='experiments'),
    path('schedule/', schedule, name='schedule'),
    path('tasks/<int:num>', tasks, name="tasks"),
    path('subtasks/<int:num>', subtasks, name="subtasks"),
    path('variations/<int:id>', variations, name="variations"),
    path('comment/<int:num>', comment, name="comment"),
    path('calendar/', calendar, name='calendar'),
]