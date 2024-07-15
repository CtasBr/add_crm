import csv
import os
from os.path import basename

# from django.conf import STATIC_ROOT
from django.contrib.auth.models import Group, User
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static

from .models import *


def take(request):
    '''
    Функция которая вызывается при взаимодействии с позициями на складе 
    Обрабатывается GET-запрос:
    take - ID взятого (-1 если не взято)
    return - ID того что вернули (-1 если ничего не вернули)
    count - количество взятого (-1 если ничего)
    '''
    take_obj = int(request.GET.get("take", "-1"))
    return_obj = int(request.GET.get("return", "-1"))
    count_obj = request.GET.get("count", "-1")
    count_obj = float(count_obj) if count_obj else -1
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
    '''
    Функция отображения склада
    Есть GET с параметром obj (передается поисковый запрос)
    Если нет поискового запроса, то показываются все объекты, если есть, то отображаются те, 
    которые подходят под поисковый запрос
    '''
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
    '''
    Функция отображения заявок на закупки
    По GET-запросу передается какой тип заявок отображать (по позициям (appl), по ТЗ (technical_specification), по оборудованию (equipment))
    '''
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
        applications = EquipmentApplication.objects.all().order_by("-id")
        equipment = Equipment.objects.all()
        data = {
            "nav": nav_state,
            "appl": applications,
            "objects": equipment,
            "status": statuses,
            "topics": topics,
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
    '''
    Функция изменения статуса и срока поставки заявки по позициям 
    Обрабатвается POST-запрос из формы
    num - ID заявки по позициям
    '''
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
    
    return redirect('purchase')

def add_application(request):
    '''
    Функция обработки формы добавления заявки по позициям
    '''
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
    '''
    Функция обработки формы добавления заявки по ТЗ
    '''
    if request.method == 'POST':
        topic = request.POST.get('topic')
        name_provider = request.POST.get('name_provider')
        contact = request.POST.get('contact')
        provider = Provider(name=name_provider, link=contact)
        provider.save()
        payment_method = "Постоплата" if request.POST.get('payment_method')=="post-payment" else "30/70"
        diadok = request.POST.get('diadok')
        filefield = request.FILES.get('ts')
        # with open(f'media/technical_specification/{filefield.name}', 'wb+') as destination:
        #         for chunk in filefield.chunks():
        #             destination.write(chunk)

        
        # print('POST: ', filefield)
        print('FILES: ', filefield, filefield.size, filefield.name)
        application = ApplicationTechnicalSpecification(purchase_topic=Purchase_topic.objects.get(id=topic), 
                                  creator=request.user, 
                                  status=Status.objects.get(id=1), 
                                  payment_form=payment_method, 
                                  provider=provider,
                                  technical_specification=filefield
                                )
        application.save()
        print(application.technical_specification)
        
    return redirect('purchase')

def add_equipment(request):
    '''
    Функция обработки формы добавления заявки по оборудованию
    '''
    if request.method == 'POST':
        topic = request.POST.get('topic')
        name_provider = request.POST.get('name_provider')
        contact = request.POST.get('contact')
        provider = Provider(name=name_provider, link=contact)
        provider.save()
        payment_method = "Постоплата" if request.POST.get('payment_method')=="post-payment" else "30/70"
        diadok = request.POST.get('diadok')
        equipments = request.POST.getlist('name_position')
        num_pos = len(equipments)
        count_pos = request.POST.getlist('count')
        link = request.POST.getlist('link')
        
        for i in range(num_pos):
            try:
                equipment = Equipment.objects.get(title=equipments[i])
            except:
                equipment = Equipment(name=equipments[i], quantity=int(count_pos[i]))
                equipment.save()
            equipments[i] = equipment
            
        application = EquipmentApplication(purchase_topic=Purchase_topic.objects.get(id=topic), 
                                  creator=request.user, 
                                  status=Status.objects.get(id=1), 
                                  payment_form=payment_method, 
                                  provider=provider
                                )

        application.save()
        
        application.equipment.set(equipments)
        
        
    return redirect('purchase')

def equipment(request, num):
    '''
    Функция изменения статуса и срока поставки заявки по оборудованию 
    Обрабатвается POST-запрос из формы
    num - ID заявки по оборудованию
    '''
    if request.method == 'POST':
        deadline = request.POST.get('deadline', None)
        status = request.POST.get('status')
        appl = EquipmentApplication.objects.get(id=num)
        appl.status = Status.objects.get(id=int(status))
        appl.deadline = deadline
        appl.save(update_fields=["status", "deadline"])
    return redirect('purchase')

def download_file(request, pk):
    print(pk)
    obj = ApplicationTechnicalSpecification.objects.get(pk=pk)
    return FileResponse(obj.technical_specification, as_attachment=True)

def update_warehouse_csv(request):
    csv_file_path = '/Users/stanislavbratkov/PycharmProjects/add_crm/add_crm/add_crm/static/sheets/warehouse_sheet.csv'
    # [name, quantity, units, min_quantity]
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        rows = []
        for row in csvreader:
            # print(row)
            if len(row) > 1:
                row[0] = row[0] + '.' + row[1]
            row[0] = row[0].split(";")
            rows.append(row[0])
        rows.pop(0)
        # title quantity units link min_quantity is_done
        for i in rows:
            print(i)
            obj = Position(title=str(i[0]), quantity=float(i[1]), units=Unit.objects.get(title=str(i[2]).lower()), min_quantity=float(i[3]), is_done=True)
            obj.save()
            
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # files = os.listdir(dir_path)
    # print(files)
    return redirect('purchase')