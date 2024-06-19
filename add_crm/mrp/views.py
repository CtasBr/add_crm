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
    if request.method == 'POST':
        contact = request.POST.get('contact')
        payment_method = request.POST.get('payment_method')
        diadok = request.POST.get('diadok')
        positions = request.POST.getlist('name_position')
        num_pos = len(positions)
        count_pos = request.POST.getlist('count')
        units = request.POST.getlist('units')
        
        for i in range(num_pos):
            try:
                position = Position.objects.get(title=positions[i])
            except:
                position = Position(title=positions[i], quantity=0, units=Unit.objects.get(id=int(units[i])), is_done = False )
                position.save()
            positions[i] = position
            print(position)
        print(f'contact {contact}, payment_method {payment_method}, diadok {diadok}, name_position {positions}, count_pos {count_pos}, units {units}')
        
    return redirect('purchase')