from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render

from .models import *


def take(request, flag):
    if request.method == 'POST':
        obj = request.POST.get('obj')
        count_units = request.POST.get('count')
        object = Position.objects.get(title=obj)
        if flag:
            object.quantity = object.quantity + float(count_units)
        else:
            object.quantity = object.quantity - float(count_units)
        actions = ["взял", "вернул"]
        object.save(update_fields=['quantity'])
        log = TraceLogUnit(user_name=request.user, object=object, count_units=count_units, action=actions[flag])
        log.save()
    return redirect('warehouse')


def warehouse(request):
    take_obj = int(request.GET.get("take", "-1"))
    return_obj = int(request.GET.get("return", "-1"))
    
    if take_obj != -1:
        take_obj = Position.objects.get(id=take_obj)
    else:
        take_obj = ""
        
    if return_obj != -1:
        return_obj = Position.objects.get(id=return_obj)
    else:
        return_obj = ""

    print(take_obj)
    obj = Position.objects.all()
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
        "take_obj": take_obj,
        "return_obj": return_obj
    }
    return render(request, "warehouse.html", data)


def purchase(request):
    applications = Application.objects.all().order_by("-id")
    nav_state = {"projects": "", 
                 "hant": "",
                 "calendar": "",
                 "employees": "",   
                 "warehouse": "", 
                 "purchase":  "active"
                 }
    
    data = {
        "nav": nav_state,
        "applications": applications,
    }
    return render(request, "purchase.html", data)
