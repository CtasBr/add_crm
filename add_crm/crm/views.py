from django.shortcuts import render

from .models import *


def projects(request):
    done_index = int(request.GET.get("done", -1))
    if done_index > -1:
        p_d = Project.objects.filter(id=done_index)
        p_d.update(is_done=True)

    p = Project.objects.all()
    data = {"projects": p}
    return render(request, 'projects.html', data)


def tasks(request, num):
    done_index = int(request.GET.get("done", -1))
    if done_index > -1:
        t_d = Task.objects.filter(id=done_index)
        t_d.update(is_done=True)

    tasks = Task.objects.filter(main_project_id=num)
    data = {"tasks": tasks}
    return render(request, 'tasks.html', data)

def subtasks(request, num):
    done_index = int(request.GET.get("done", -1))
    if done_index > -1:
        st_d = Subtask.objects.filter(id=done_index)
        st_d.update(is_done=True)
        
    subtasks = Subtask.objects.filter(main_task_id=num)
    data = {"subtasks": subtasks}
    
    return render(request, 'subtasks.html', data)

def experiments(request):
    return render(request, 'experiments.html')


def schedule(request):
    return render(request, 'schedule.html')


# Create your views here.
