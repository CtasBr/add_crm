from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import *


def projects(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        deadline = request.POST.get('deadline')
        description = request.POST.get('description')
        print(title, deadline, description)
        project = Project(title=title, deadline=deadline, description=description, is_done=False)
        project.save()  # Сохраняем объект в базе данных

        return redirect('projects')


    
    done_index = int(request.GET.get("done", -1))
    if done_index > -1:
        p_d = Project.objects.filter(id=done_index)
        p_d.update(is_done=True)

    p = Project.objects.all()
    data = {"projects": p}
    return render(request, 'projects.html', data)


def tasks(request, num):
    if request.method == 'POST':
        title = request.POST.get('title')
        deadline = request.POST.get('deadline')
        description = request.POST.get('description')
        users = request.POST.getlist('users')
        print(title, deadline, description, users)
        task = Task(title=title, deadline=deadline, description=description, is_done=False, main_project_id=Project.objects.get(id=num))
        users = User.objects.filter(id__in=users)
        task.save()
        task.executors_id.set(users)
          # Сохраняем объект в базе данных

        return redirect('tasks', num)
    
    done_index = int(request.GET.get("done", -1))
    if done_index != -1:
        t_d = Task.objects.filter(id=done_index)
        t_d.update(is_done=True)
    
    s_done_index = int(request.GET.get("done_subtask", -1))
    print(s_done_index)
    if s_done_index != -1:
        s_d = Subtask.objects.filter(id=s_done_index)
        s_d.update(is_done=True)
    
    subtasks = Subtask.objects.all()
    tasks = Task.objects.filter(main_project_id=num)
    users = User.objects.all()
    data = {"tasks": tasks, "users": users, "subtasks": subtasks}
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
