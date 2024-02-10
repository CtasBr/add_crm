from django.contrib import admin

from .models import Subtask, Task, User

admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(User)

