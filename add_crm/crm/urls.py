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
    path('edit_task/<int:num>', edit_task, name="edit_task"),
    path('edit_project/<int:num>', edit_project, name="edit_project"),
    path('calendar/', calendar, name='calendar'),
    path('gantt/', gantt, name='gantt'),
    path('staff/', staff, name='staff'),
    path('add_res_document/<int:num>', add_result, name='add_result'),
    path('download_file/<int:pk>', download_file, name="download_file"),
    path('result/<int:num>', result, name="result")
]