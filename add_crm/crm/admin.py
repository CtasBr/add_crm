from django.contrib import admin

from .models import Comment, Experiment, Project, Subtask, Task, User, Variation

admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Experiment)
admin.site.register(Variation)
admin.site.register(Comment)