import calendar as cal
import datetime
import locale
import math
import random

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import *


def generate_random_hex():
    random_number = random.randrange(0, 16777215) 
    hex_number = hex(random_number)[2:]
    res_hex = ['0', '0', '0', '0', '0', '0']
    for i in range(-1, -1*len(hex_number)-1, -1):
        res_hex[i] = hex_number[i]
    res_hex = '#' + ''.join(res_hex)
    return res_hex


def projects(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        deadline = request.POST.get('deadline')
        date_start = request.POST.get('date_start')
        description = request.POST.get('description')
        project = Project(title=title, deadline=deadline, description=description, is_done=False, date_add=date_start)
        project.save()  # Сохраняем объект в базе данных

        return redirect('projects')


    
    done_task_index = int(request.GET.get("done_task", -1))
    if done_task_index > -1:
        t_d = Task.objects.filter(id=done_task_index)
        t_d.update(is_done=True)
    
    done_subtask_index = int(request.GET.get("done_subtask", -1))
    print(done_subtask_index)
    if done_subtask_index > -1:
        st_d = Subtask.objects.filter(id=done_subtask_index)
        st_d.update(is_done=True)
    nav_state = {"projects": "active", 
                 "hant": "",
                 "calendar": "",
                 "employees": ""    
                 }

    
    p = Project.objects.all()
    t = Task.objects.all()
    s = Subtask.objects.all()
    u = Empl.objects.all()
    c = Comment.objects.all()
    data = {"projects": p, 
            "tasks": t, 
            "subtasks": s,
            "users": u,
            "comments": c,
            "nav": nav_state,
            }
    return render(request, 'index.html', data)


def tasks(request, num):
    if request.method == 'POST':
        title = request.POST.get('title')
        deadline = request.POST.get('deadline')
        description = request.POST.get('description')
        users = request.POST.getlist('users')
        date_start = request.POST.get('date_start')
        task = Task(title=title, deadline=deadline, description=description, is_done=False, main_project_id=Project.objects.get(id=num), date_add=date_start)
        users = User.objects.filter(id__in=users)
        task.save()
        task.executors_id.set(users)

        return redirect('projects')

def subtasks(request, num):
    if request.method == 'POST':
        title = request.POST.get('title')
        deadline = request.POST.get('deadline')
        date_start = request.POST.get('date_start')
        subtask = Subtask(title=title, deadline=deadline, is_done=False, main_task_id=Task.objects.get(id=num), date_add=date_start)
        subtask.save()
        return redirect('projects')

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
    lvl = int(request.GET.get("lvl", 1))
    gant_data = []
    if lvl == 1:
        lvl_name = "Проекты"
        projects = Project.objects.filter(is_done=False).order_by("date_add")
        for p in projects:
            done_tasks = Task.objects.filter(main_project_id__id=p.id).filter(is_done=True)
            all_tasks = Task.objects.filter(main_project_id__id=p.id)
            if len(all_tasks) != 0:
                percent = len(done_tasks)/len(all_tasks) * 100
            else:
                percent = 100
                
            start_date = datetime.datetime.combine(p.date_add, datetime.datetime.min.time())
            end_date = datetime.datetime.combine(p.deadline, datetime.datetime.min.time())
            buf_lst = [str(p.id), 
                       str(p.title), 
                       str(p.id), 
                          {"d": int(start_date.day), 
                          "m": int(start_date.month),
                          "y": int(start_date.year)
                          },
                          {"d": int(end_date.day), 
                          "m": int(end_date.month),
                          "y": int(end_date.year)
                          },
                       percent,
                        ]
            gant_data.append(buf_lst)
        
    elif lvl == 2:
        lvl_name = "Задачи"
        tasks = Task.objects.filter(is_done=False).order_by("date_add")
        for t in tasks:
            done_tasks = Subtask.objects.filter(main_task_id__id=t.id).filter(is_done=True)
            all_tasks = Subtask.objects.filter(main_task_id__id=t.id)
            if len(all_tasks) != 0:
                percent = len(done_tasks)/len(all_tasks) * 100
            else:
                percent = 100
            start_date = datetime.datetime.combine(t.date_add, datetime.datetime.min.time())
            end_date = datetime.datetime.combine(t.deadline, datetime.datetime.min.time())
            buf_lst = [str(t.id), 
                       str(t.title), 
                       str(t.main_project_id.title), 
                          {"d": int(start_date.day), 
                          "m": int(start_date.month),
                          "y": int(start_date.year)
                          },
                          {"d": int(end_date.day), 
                          "m": int(end_date.month),
                          "y": int(end_date.year)
                          },
                       percent,
                        ]
            gant_data.append(buf_lst)
    
    elif lvl == 3:
        lvl_name = "Подзадачи"
        tasks = Subtask.objects.filter(is_done=False).order_by("date_add")
        for t in tasks:    
            percent = 0
            start_date = datetime.datetime.combine(t.date_add, datetime.datetime.min.time())
            end_date = datetime.datetime.combine(t.deadline, datetime.datetime.min.time())
            buf_lst = [str(t.id), 
                       str(t.title), 
                       str(t.main_task_id.main_project_id.title), 
                          {"d": int(start_date.day), 
                          "m": int(start_date.month),
                          "y": int(start_date.year)
                          },
                          {"d": int(end_date.day), 
                          "m": int(end_date.month),
                          "y": int(end_date.year)
                          },
                       percent,
                        ]
            gant_data.append(buf_lst)
    gant_height = len(gant_data) * 50  
    
    now = datetime.datetime.now()
    r_year = request.GET.get("year", now.year)
    r_month = request.GET.get("month", now.month)
    # calendar = generate_calendar(int(r_month), int(r_year))
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
    
    users_info = []
    users = User.objects.all()
    
    for u in users:
        tasks = Task.objects.filter(executors_id=u.id).filter(is_done=False)
        users_info.append([u, len(tasks), tasks])
    
    
    data = {"calendar": calendar, 
            "date": [int(r_year), int(r_month)],
            "gant": gant_data,
            "gant_height": gant_height,
            "lvl": lvl_name,
            "users": users_info,
            }
    
    return render(request, 'schedule.html', data)


def comment(request, num):
    if request.method == 'POST':
        text = request.POST.get('text')
        # file = request.POST.get('file')
        comment = Comment(text=text, main_task_id=Task.objects.get(id=num), user=request.user)
        comment.save()
        return redirect('projects')
    
def calendar(request):
    subtasks = Subtask.objects.all()
    tasks = Task.objects.all()
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    today = datetime.date.today()
    day_word = today.strftime('%A')
    day_number = today.strftime('%d')  # число
    month_word = today.strftime('%B')  # месяц
    year = today.strftime('%Y')  # год
    date = {"day": day_word.capitalize(), 
            "day_num": day_number, 
            "month": month_word.capitalize(),
            "year": year
            }
    r_year = int(request.GET.get("year", today.year))
    r_month = int(request.GET.get("month", today.month))
    c = cal.monthcalendar(r_year, r_month)
    translate = ["first", "second", "third", "fourth", "fifth", "sixth"]
    c_done = []
    
    subtask_dates = []
    subtask_names = []
    for i in subtasks:
        dates = datetime.datetime.combine(i.deadline, datetime.datetime.min.time())
        if int(dates.month) == int(r_month) and int(dates.year) == int(r_year):
            subtask_dates.append(dates.day)
            subtask_names.append(i.title)
    task_dates = []
    task_names = []
    for i in tasks:
            dates = datetime.datetime.combine(i.deadline, datetime.datetime.min.time())
            if int(dates.month) == int(r_month) and int(dates.year) == int(r_year):
                task_dates.append(dates.day)
                task_names.append(i.title)
        
    used = {"task": 0, "subtask":0}
    for week in c:
        for i in range(len(week)):
            if week[i] in task_dates:
                week[i] = {"ev": f"{task_names[used['task']]}", "date": week[i]}
                used["task"] += 1
            elif week[i] in subtask_dates:
                week[i] = {"ev": f"{subtask_names[used['subtask']]}", "date": week[i]}
                used["subtask"] += 1
            else:
                week[i] = {"ev": "", "date": week[i]}
    
    for i in range(len(c)):
        c_done.append({"text": translate[i], "week": c[i]})
    nav_state = {"projects": "", 
                 "hant": "",
                 "calendar": "active",
                 "employees": ""    
                 }
    date_active = {
        "year": r_year,
        "month": r_month,
    }
    
    data = {
        "date": date,
        "calendar": c_done,
        "nav": nav_state,
        "date_active": date_active,
    }
    return render(request, 'calendar.html', data)

range_lvl = "week"
lvl = "projects"

def gantt(request):
    global range_lvl
    global lvl
    range_lvl = request.GET.get("range", range_lvl)
    lvl = request.GET.get("lvl", lvl)
    column_names= [i for i in range(1, 32)]
    button_state = {"projects": "", "tasks": ""}
    button_state[lvl] = "active"
    current_date = datetime.datetime.now()
    current_year = int(request.GET.get("year", current_date.year))
    current_month = int(request.GET.get("month", current_date.month))
    month_start = f"1.{current_month}.{current_year}"
    month_name = [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    date_active = {"year": current_year, "month": current_month, "month_name": month_name[current_month-1]}
    if current_month != 12: 
        month_end = f"1.{current_month+1}.{current_year}"
    else:
        month_end = f"1.1.{current_year+1}"
    month_start = datetime.datetime.strptime(month_start, '%d.%m.%Y')
    month_end = datetime.datetime.strptime(month_end, '%d.%m.%Y')
    line_inf = []
    if lvl == "projects":
        projects_inf = Project.objects.filter(deadline__gte=month_start, date_add__lte=month_end, is_done=False)
        for i in projects_inf:
            second_layer = []
            get_tasks = Task.objects.filter(deadline__gte=month_start, date_add__lte=month_end, main_project_id=i, is_done=False)
            for y in get_tasks:
                second_layer.append({"title": y.title,
                                     "hint": f"с {y.date_add.strftime('%d.%m.%Y')} по {y.deadline.strftime('%d.%m.%Y')}",
                                     "start_tag": "1" if y.date_add.month < current_month or y.deadline.year < current_year else y.date_add.day, 
                                     "end_tag": "31" if y.deadline.month > current_month or y.deadline.year > current_year else y.deadline.day})
            first_layer = {
                "title": i.title,
                "hint": f"с {i.date_add.strftime('%d.%m.%Y')} по {i.deadline.strftime('%d.%m.%Y')}",
                "start_tag": "1" if i.date_add.month < current_month or i.deadline.year < current_year else i.date_add.day, 
                "end_tag": "31" if i.deadline.month > current_month or i.deadline.year > current_year else i.deadline.day
            }
            line_inf.append({"color": generate_random_hex(),
                             "first_layer": first_layer,
                             "second_layer": second_layer})
    elif lvl == "tasks":
        task_inf = Task.objects.filter(deadline__gte=month_start, date_add__lte=month_end, is_done=False)
        for i in task_inf:
            second_layer = []
            get_subtasks = Subtask.objects.filter(deadline__gte=month_start, date_add__lte=month_end, main_task_id=i, is_done=False)
            for y in get_subtasks:
                second_layer.append({"title": y.title,
                                     "hint": f"с {y.date_add.strftime('%d.%m.%Y')} по {y.deadline.strftime('%d.%m.%Y')}",
                                     "start_tag": "1" if y.date_add.month < current_month or y.deadline.year < current_year else y.date_add.day, 
                                     "end_tag": "31" if y.deadline.month > current_month or y.deadline.year > current_year else y.deadline.day})
            first_layer = {
                "title": i.title,
                "hint": f"с {i.date_add.strftime('%d.%m.%Y')} по {i.deadline.strftime('%d.%m.%Y')}",
                "start_tag": "1" if i.date_add.month < current_month or i.deadline.year < current_year else i.date_add.day, 
                "end_tag": "31" if i.deadline.month > current_month or i.deadline.year > current_year else i.deadline.day
            }
            line_inf.append({"color": generate_random_hex(), 
                             "first_layer": first_layer, 
                             "second_layer": second_layer})
        
        
    print(line_inf)
    nav_state = {"projects": "", 
                 "hant": "active",
                 "calendar": "",
                 "employees": ""    
                 }
    print(line_inf)
    data = {
        "nav": nav_state,
        "b_s": button_state,
        "c_n": column_names,
        "infos": line_inf,
        "date_active": date_active,
    }
    return render(request, 'gantt.html', data)


def staff(request):
    users = Empl.objects.all()
    counter = 0
    users_infos = {
        "part1": [],
        "part2": [],
        "part3": [],
    }
    
    for i in users:
        if len(users_infos["part1"]) < math.ceil(len(users)/3):
            users_infos["part1"].append({"usr": i})
        elif len(users_infos["part2"]) < math.ceil((len(users) - len(users_infos["part2"]))/2):
            users_infos["part2"].append(i)
        else:
            users_infos["part3"].append(i)
    print(users_infos)
        
    nav_state = {"projects": "", 
                 "hant": "",
                 "calendar": "",
                 "employees": "active"    
                 }
    data = {
        "nav": nav_state,
    }
    return render(request, "staff.html", data)