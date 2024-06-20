from os.path import basename

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
    types = request.GET.get("type", "appl")
    topics = Purchase_topic.objects.all()
    statuses = Status.objects.all()
    if types == "appl":
        applications = Application.objects.all().order_by("-id")
        units = Unit.objects.all()
        
        obj_for_add = Position.objects.all()
        
    nav_state = {"projects": "", 
                 "hant": "",
                 "calendar": "",
                 "employees": "",   
                 "warehouse": "", 
                 "purchase":  "active"
                 }
    if types == "appl":
        data = {
            "nav": nav_state,
            "appl": applications,
            "units": units,
            "status": statuses,
            "objects": obj_for_add,
            "topics": topics,
        }
        return render(request, "purchase.html", data)

    elif types == "equipment":
        applications = EquipmentApplication.objects.all()
        data = {
            "nav": nav_state,
            "appl": applications,
        }
        return render(request, "purchase_e.html", data)
    
    else:
        applications = ApplicationTechnicalSpecification.objects.all().order_by("-id")
        data = {
            "nav": nav_state,
            "appl": applications,
            "status": statuses,
            "topics": topics,
        }
        return render(request, "purchase_t.html", data)
    


def application(request, num):
    if request.method == 'POST':
        deadline = request.POST.get('deadline', None)
        status = request.POST.get('status')
        appl = Application.objects.get(id=num)
        appl.status = Status.objects.get(id=int(status))
        appl.deadline = deadline
        if appl.status.id == 5:
            for pos in appl.positions.all():
                obj = pos.position
                update_fields=["is_done"]
                if obj.units == pos.units:
                    obj.quantity += pos.quantity
                    update_fields.append("quantity")
                elif (obj.units.title == "кг" and pos.units.title == "г") or (obj.units.title == "л" and pos.units.title == "мл"):
                    obj.quantity += (pos.quantity / 1000)
                    update_fields.append("quantity")
                elif (obj.units.title == "г" and pos.units.title == "кг") or (obj.units.title == "мл" and pos.units.title == "л"):
                    obj.quantity += (pos.quantity * 1000)
                    update_fields.append("quantity")
                else:
                    pass
                obj.is_done = True
                obj.save(update_fields=update_fields)
        appl.save(update_fields=["status", "deadline"])
        print("a", deadline)
    
    return redirect('purchase')


def add_application(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        name_provider = request.POST.get('name_provider')
        contact = request.POST.get('contact')
        provider = Provider(name=name_provider, link=contact)
        provider.save()
        payment_method = "Постоплата" if request.POST.get('payment_method')=="post-payment" else "30/70"
        diadok = request.POST.get('diadok')
        positions = request.POST.getlist('name_position')
        num_pos = len(positions)
        count_pos = request.POST.getlist('count')
        units = list(map(int, request.POST.getlist('units')))
        link = request.POST.getlist('link')
        min_count = list(map(int, request.POST.getlist('min_count')))
        
        for i in range(num_pos):
            try:
                position = Position.objects.get(title=positions[i])
                print(min_count[i] != position.min_quantity, int(units[i]) == position.units.id)
                if min_count[i] != position.min_quantity and units[i] == position.units.id:
                    print("done_ifff")
                    position.min_quantity = min_count[i]
                    position.save(update_fields=["min_quantity"])
            except:
                position = Position(title=positions[i], quantity=0, units=Unit.objects.get(id=int(units[i])), is_done = False )
                position.save()
            positions[i] = PositionInApplication(position=position, quantity=int(count_pos[i]), link=link[i], units=Unit.objects.get(id=int(units[i])))
            positions[i].save()
        # print(f'contact {contact}, payment_method {payment_method}, diadok {diadok}, name_position {positions}, count_pos {count_pos}, units {units}')
        
        application = Application(purchase_topic=Purchase_topic.objects.get(id=topic), 
                                  creator=request.user, 
                                  status=Status.objects.get(id=1), 
                                  payment_form=payment_method, 
                                  provider=provider
                                )
        application.save()
        application.positions.set(positions)
        
    return redirect('purchase')


def add_application_ts(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        name_provider = request.POST.get('name_provider')
        contact = request.POST.get('contact')
        provider = Provider(name=name_provider, link=contact)
        provider.save()
        payment_method = "Постоплата" if request.POST.get('payment_method')=="post-payment" else "30/70"
        diadok = request.POST.get('diadok')
        filefield = request.POST.get('file')
        application = ApplicationTechnicalSpecification(purchase_topic=Purchase_topic.objects.get(id=topic), 
                                  creator=request.user, 
                                  status=Status.objects.get(id=1), 
                                  payment_form=payment_method, 
                                  provider=provider,
                                  technical_specification=filefield
                                )
        application.save()
        
    return redirect('purchase')