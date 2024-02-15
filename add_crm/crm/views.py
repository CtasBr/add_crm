import calendar
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import *


def generate_calendar(month, year):
    # Получаем количество дней в указанном месяце и году
    num_days = calendar.monthrange(year, month)[1]
    
    # Получаем день недели первого дня указанного месяца
    first_day_weekday = calendar.weekday(year, month, 1)
    
    # Создаем список-календарь с пустыми ячейками
    calendar_list = [["" for _ in range(7)] for _ in range(6)]
    
    # Заполняем список-календарь днями месяца
    current_day = 1
    for week in range(6):
        for weekday in range(7):
            if current_day <= num_days and (week > 0 or weekday >= first_day_weekday):
                calendar_list[week][weekday] = [str(current_day)]
                current_day += 1
    
    return calendar_list



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
    if s_done_index != -1:
        s_d = Subtask.objects.filter(id=s_done_index)
        s_d.update(is_done=True)
    
    subtasks = Subtask.objects.all()
    tasks = Task.objects.filter(main_project_id=num)
    users = User.objects.all()
    data = {"tasks": tasks, 
            "users": users, 
            "subtasks": subtasks
            }
    return render(request, 'tasks.html', data)

def subtasks(request, num):
    if request.method == 'POST':
        title = request.POST.get('title')
        deadline = request.POST.get('deadline')
        subtask = Subtask(title=title, deadline=deadline, is_done=False, main_task_id=Task.objects.get(id=num))
        subtask.save()
        return redirect('tasks', subtask.main_task_id.main_project_id.id)

def experiments(request, id):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        experiment = Experiment(title = title, instruction=description, main_project_id=Project(id=id))
        experiment.save()
        
    
    experiments = Experiment.objects.filter(main_project_id=id)
    variations = Variation.objects.all()
    data = {"experiments": experiments, 
            "variations": variations
            }
    
    return render(request, 'experiments.html', data)


def variations(request, id):
    if request.method == 'POST':
        code = request.POST.get('title')
        date_start = request.POST.get('date_start')
        date_end = request.POST.get('deadline')
        comment = request.POST.get('comment')
        content = request.POST.get('changes')
        variation = Variation(code=code, date_start=date_start, date_end=date_end, comment=comment, content=content, main_experiment_id=Experiment.objects.get(id=id))
        variation.save()
        return redirect('experiments', variation.main_experiment_id.main_project_id.id)

def schedule(request):
    now = datetime.datetime.now()
    r_year = request.GET.get("year", now.year)
    r_month = request.GET.get("month", now.month)
    print(r_month)
    print(r_year)
    calendar = generate_calendar(int(r_month), int(r_year))
    subtasks = Subtask.objects.all()
    tasks = Task.objects.all()
    projects = Project.objects.all()
    buf = []
    for i in subtasks:
        dates = datetime.datetime.combine(i.deadline, datetime.datetime.min.time())
        if int(dates.month) == int(r_month) and int(dates.year) == int(r_year):
            buf.append(dates.day)
    for i in range(len(calendar)):
        for j in range(len(calendar[i])):
            try:
                if int(calendar[i][j][0]) in buf:
                    calendar[i][j].append(True)
                else:
                    calendar[i][j].append(False)
            except IndexError:
                continue
    buf = []
    for i in tasks:
        dates = datetime.datetime.combine(i.deadline, datetime.datetime.min.time())
        if int(dates.month) == int(r_month) and int(dates.year) == int(r_year):
            buf.append(dates.day)
    for i in range(len(calendar)):
        for j in range(len(calendar[i])):
            try:
                if int(calendar[i][j][0]) in buf:
                    calendar[i][j].append(True)
                else:
                    calendar[i][j].append(False)
            except IndexError:
                continue        
    buf = []
    for i in projects:
        dates = datetime.datetime.combine(i.deadline, datetime.datetime.min.time())
        if int(dates.month) == int(r_month) and int(dates.year) == int(r_year):
            buf.append(dates.day)
    for i in range(len(calendar)):
        for j in range(len(calendar[i])):
            try:
                if int(calendar[i][j][0]) in buf:
                    calendar[i][j].append(True)
                else:
                    calendar[i][j].append(False)
            except IndexError:
                continue
    data = {"calendar": calendar, 
            "date": [int(r_year), int(r_month)]
            }
    return render(request, 'schedule.html', data)



# Create your views here.
