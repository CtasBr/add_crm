from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render

from .models import *


def take(request):
    take_obj = int(request.GET.get("take", "-1"))
    return_obj = int(request.GET.get("return", "-1"))
    count_obj = request.GET.get("count", "-1")
    count_obj = float(count_obj) if count_obj else -1

    print(take_obj, return_obj, count_obj)
    id_obj = max(take_obj, return_obj)
    print(id_obj)
    if id_obj>=0 and count_obj>0:
        object = Position.objects.get(id=id_obj)
        if take_obj > -1:
            object.quantity = object.quantity - count_obj
            flag = 0
        else:
            object.quantity = object.quantity + count_obj
            flag = 1
        object.save(update_fields=['quantity'])
        actions = ["взял", "вернул"]
        log = TraceLogUnit(user_name=request.user, object=object, count_units=count_obj, action=actions[flag])
        log.save()
    return redirect('warehouse')


def warehouse(request):
    find = request.GET.get("obj", "")
    if find:
        obj = Position.objects.filter(title__icontains=find.lower())
    else:
        obj = Position.objects.all()
    obj_for_find = Position.objects.all()
    nav_state = {"projects": "", 
                 "hant": "",
                 "calendar": "",
                 "employees": "",   
                 "warehouse": "active",
                 "purchase":  ""   
                 }
    data = {
        "nav": nav_state,
        "positions": obj,
        "find": find,
        "find_objs": obj_for_find,
    }
    return render(request, "warehouse.html", data)


def purchase(request):
    applications = Application.objects.all().order_by("-id")
    units = Unit.objects.all()
    statuses = Status.objects.all()
    obj_for_add = Position.objects.all()
    nav_state = {"projects": "", 
                 "hant": "",
                 "calendar": "",
                 "employees": "",   
                 "warehouse": "", 
                 "purchase":  "active"
                 }
    
    data = {
        "nav": nav_state,
        "appl": applications,
        "units": units,
        "status": statuses,
        "objects": obj_for_add
    }
    return render(request, "purchase.html", data)


def application(request, num):
    if request.method == 'POST':
        deadline = request.POST.get('deadline')
        status = request.POST.get('status')
        appl = Application.objects.get(id=num)
        appl.status = Status.objects.get(id=int(status))
        appl.deadline = deadline
        if appl.status.id == 5:
            for pos in appl.positions.all():
                obj = pos.position
                obj.quantity += pos.quantity
                obj.save(update_fields=["quantity"])
        appl.save(update_fields=["status", "deadline"])
        print("a", deadline)
    
    return redirect('purchase')


def add_application(request):
    print("OK done")
    return redirect('purchase')