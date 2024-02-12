from django.contrib import admin

from .models import Project, Subtask, Task, User

admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(User)
admin.site.register(Project)