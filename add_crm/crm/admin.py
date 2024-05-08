from django.contrib import admin

from .models import Comment, Empl, Experiment, Project, Subtask, Task, Variation

admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(Empl)
admin.site.register(Project)
admin.site.register(Experiment)
admin.site.register(Variation)
admin.site.register(Comment)