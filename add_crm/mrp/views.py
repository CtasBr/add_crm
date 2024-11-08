import csv
import os
import random
from os.path import basename

from django.contrib.auth.models import Group, User
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.urls import include, path

from .models import *

# {"path": {"is_used": (boolean), "purchase_type": (int), "purchase_id": (int)}}
# 1 - appl; 2 - eq; 3 - ts

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
    user_info = {
            "AddLab": request.user.groups.filter(name='AddLab').exists() if request.user.is_authenticated else False,
            "CaramLab": request.user.groups.filter(name='Ceramist').exists() if request.user.is_authenticated else False,
            "PurS": request.user.groups.filter(name='purchasing_specialist').exists() if request.user.is_authenticated else False,
        }
    '''
    Функция отображения склада
    Есть GET с параметром obj (передается поисковый запрос)
    Если нет поискового запроса, то показываются все объекты, если есть, то отображаются те, 
    которые подходят под поисковый запрос
    '''
    find = request.GET.get("obj", "")
    if find:
        obj = Position.objects.filter(title__icontains=find)
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
        "user_info": user_info
    }
    return render(request, "warehouse.html", data)

def purchase(request, link):
    last_obj = Path.objects.order_by('-id').first()
    req_path = request.path.replace('/purchase', '', 1)
    last_path = f'{req_path}/{last_obj}'
    link_name = 'purchase'
    if link == "purchase":
        add_link_name = "add_application"
        user_info = {
            "AddLab": request.user.groups.filter(name='AddLab').exists() if request.user.is_authenticated else False,
            "CaramLab": request.user.groups.filter(name='Ceramist').exists() if request.user.is_authenticated else False,
            "PurS": request.user.groups.filter(name='purchasing_specialist').exists() if request.user.is_authenticated else False,
            "CanAddPath": request.user.groups.filter(name='adder_path').exists() if request.user.is_authenticated else False,
        }
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
            units_by_obj = {}
            for i in obj_for_add:
                units_by_obj[i.title] = i.units
            
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
                "user_info": user_info,
                "units_by_obj": units_by_obj,
                "link_name": link_name,
                "add_link_name": add_link_name,
                "last_path": last_path,
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
                "user_info": user_info,
                "link_name": link_name,
                "add_link_name": add_link_name,
            }
            return render(request, "purchase_e.html", data)
        
        else:
            applications = ApplicationTechnicalSpecification.objects.all().order_by("-id")
            data = {
                "nav": nav_state,
                "appl": applications,
                "status": statuses,
                "topics": topics,
                "user_info": user_info,
                "link_name": link_name,
                "add_link_name": add_link_name
            }
            return render(request, "purchase_t.html", data)
    else:
        user_info = {
            "AddLab": request.user.groups.filter(name='AddLab').exists() if request.user.is_authenticated else False,
            "CaramLab": request.user.groups.filter(name='Ceramist').exists() if request.user.is_authenticated else False,
            "PurS": request.user.groups.filter(name='purchasing_specialist').exists() if request.user.is_authenticated else False,
            "CanAddPath": request.user.groups.filter(name='adder_path').exists() if request.user.is_authenticated else False,
        }
        '''
        Функция отображения заявок на закупки
        По GET-запросу передается какой тип заявок отображать (по позициям (appl), по ТЗ (technical_specification), по оборудованию (equipment))
        '''
        types = request.GET.get("type", "appl")
        statuses = Status.objects.all()
        link_name = link
        gen_paths = Path.objects.get(path=link_name)
        if types == "appl":
            applications = []
            can_add = False
            if gen_paths.is_used and gen_paths.purchase_type == 1:
                applications = Application.objects.get(id=gen_paths.purchase_id)
            elif not gen_paths.is_used:
                can_add = True

            units = Unit.objects.all()
            data = {
                "a": applications,
                "units": units,
                "status": statuses,
                "user_info": user_info,
                "can_add": can_add,
                "link_name": link_name,
                "add_link_name": f"add_application__{link_name}"
            }
            return render(request, "purchase.html", data)

        elif types == "equipment":
            applications = []
            can_add = False
            if gen_paths.is_used and gen_paths.purchase_type == 2:
                applications = EquipmentApplication.objects.get(id=gen_paths.purchase_id)
            elif not gen_paths.is_used:
                can_add = True
            data = {
                "a": applications,
                "status": statuses,
                "user_info": user_info,
                "can_add": can_add,
                "link_name": link_name,
                "add_link_name": f"add_equipment__{link_name}"
            }
            return render(request, "purchase_e.html", data)
        
        else:
            applications = []
            can_add = False
            if gen_paths.is_used and gen_paths.purchase_type == 3:
                applications = ApplicationTechnicalSpecification.objects.get(id=gen_paths.purchase_id)
            elif not gen_paths.is_used:
                can_add = True
            data = {
                "a": applications,
                "status": statuses,
                "user_info": user_info,
                "can_add": can_add,
                "link_name": link_name,
                "add_link_name": f"add_application_ts__{link_name}"
            }
            return render(request, "purchase_t.html", data)


def application(request, num):
    '''
    Функция изменения статуса и срока поставки заявки по позициям 
    Обрабатвается POST-запрос из формы
    num - ID заявки по позициям
    '''
    if request.method == 'POST':
        fields = ["status"]
        deadline = request.POST.get('deadline', None)
        status = request.POST.get('status')
        appl = Application.objects.get(id=num)
        appl.status = Status.objects.get(id=int(status))
        if deadline:
            fields.append('deadline')
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
                link = Link(link=pos.link, appl=appl)
                link.save()
                obj.is_done = True
                obj.save(update_fields=update_fields)
        appl.save(update_fields=fields)
    
    return redirect('purchase', 'purchase')

def add_application(request, link):
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
        link_obj = request.POST.getlist('link')
        min_count = list(map(float, request.POST.getlist('min_count')))
        
        for i in range(num_pos):
            try:
                position = Position.objects.get(title=positions[i])
                if min_count[i] != position.min_quantity and units[i] == position.units.id:
                    position.min_quantity = min_count[i]
                    position.save(update_fields=["min_quantity"])
            except:
                position = Position(title=positions[i], quantity=0, units=Unit.objects.get(id=int(units[i])), is_done = False )
                position.save()
            positions[i] = PositionInApplication(position=position, quantity=float(count_pos[i]), link=link_obj[i], units=Unit.objects.get(id=int(units[i])))
            positions[i].save()
        topic = Purchase_topic.objects.get(id=topic) if link == "add_application" else Purchase_topic.objects.get(title="Одноразовая")
        user = request.user if link == "add_application" else None
        application = Application(purchase_topic=topic, 
                                  creator=user, 
                                  status=Status.objects.get(id=1), 
                                  payment_form=payment_method, 
                                  provider=provider
                                )
        application.save()
        application.positions.set(positions)
        if link != "add_application":
            path_adding = link
            gen_paths = Path.objects.get(path=path_adding)
            gen_paths.is_used = True
            gen_paths.purchase_id = application.id
            gen_paths.purchase_type = 1
            gen_paths.save()
            
        
    return redirect("purchase", link)

def add_application_ts(request, link):
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
        
        topic = Purchase_topic.objects.get(id=topic) if link == "add_application" else Purchase_topic.objects.get(title="Одноразовая")
        user = request.user if link == "add_application" else None
        application = ApplicationTechnicalSpecification(purchase_topic=topic, 
                                  creator=user, 
                                  status=Status.objects.get(id=1), 
                                  payment_form=payment_method, 
                                  provider=provider,
                                  technical_specification=filefield
                                )
        application.save()
        
        if link != "add_application":
            path_adding = link
            gen_paths = Path.objects.get(path=path_adding)
            gen_paths.is_used = True
            gen_paths.purchase_id = application.id
            gen_paths.purchase_type = 3
            gen_paths.save()
        
    return redirect("purchase", link)

def add_equipment(request, link):
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
        link_obj = request.POST.getlist('link')
        for i in range(num_pos):
            try:
                equipment = Equipment.objects.get(title=equipments[i])
            except:
                equipment = Equipment(name=equipments[i], quantity=int(count_pos[i]), link=link_obj[i])
                equipment.save()
            equipments[i] = equipment
        topic = Purchase_topic.objects.get(id=topic) if link == "purchase" else Purchase_topic.objects.get(title="Одноразовая")
        user = request.user if link == "add_application" else None
        application = EquipmentApplication(purchase_topic=topic, 
                                  creator=user, 
                                  status=Status.objects.get(id=1), 
                                  payment_form=payment_method, 
                                  provider=provider
                                )

        application.save()
        
        application.equipment.set(equipments)
        if link != "purchase":
            path_adding = link
            gen_paths = Path.objects.get(path=path_adding)
            gen_paths.is_used = True
            gen_paths.purchase_id = application.id
            gen_paths.purchase_type = 2
            gen_paths.save()
        
        
    return redirect("purchase", link)

def equipment(request, num):
    '''
    Функция изменения статуса и срока поставки заявки по оборудованию 
    Обрабатвается POST-запрос из формы
    num - ID заявки по оборудованию
    '''
    if request.method == 'POST':
        fields = ["status"]
        deadline = request.POST.get('deadline', None)
        status = request.POST.get('status')
        appl = EquipmentApplication.objects.get(id=num)
        appl.status = Status.objects.get(id=int(status))
        if deadline: 
            appl.deadline = deadline
            fields.append("deadline")
        appl.save(update_fields=fields)
    return redirect('purchase', 'purchase')

def techical_specification(request, num):
    '''
    Функция изменения статуса и срока поставки заявки по ТЗ 
    Обрабатвается POST-запрос из формы
    num - ID заявки по оборудованию
    '''
    if request.method == 'POST':
        fields = ["status"]
        deadline = request.POST.get('deadline', None)
        status = request.POST.get('status')
        appl = ApplicationTechnicalSpecification.objects.get(id=num)
        appl.status = Status.objects.get(id=int(status))
        if deadline:
            fields.append("deadline")
            appl.deadline = deadline
        appl.save(update_fields=fields)
    return redirect('purchase', 'purchase')

def download_file(request, pk):
    obj = ApplicationTechnicalSpecification.objects.get(pk=pk)
    return FileResponse(obj.technical_specification, as_attachment=True)

def update_warehouse_csv(request):
    '''
    Function which helps add info about products by csv table (use only whis debug = False)
    '''
    csv_file_path = '/Users/stanislavbratkov/PycharmProjects/add_crm/add_crm/add_crm/static/sheets/warehouse_sheet.csv'
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        rows = []
        for row in csvreader:
            if len(row) > 1:
                row[0] = row[0] + '.' + row[1]
            row[0] = row[0].split(";")
            rows.append(row[0])
        rows.pop(0)
        for i in rows:
            obj = Position(title=str(i[0]), quantity=float(i[1]), units=Unit.objects.get(title=str(i[2]).lower()), min_quantity=float(i[3]), is_done=True)
            obj.save()
    return redirect('purchase')

def generate_random_string(length, characters):
    return ''.join(random.choices(characters, k=length))


def gen_path(request):
    length = 16
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    
    random_string = generate_random_string(length, characters)
    gen_paths = Path(path=random_string, is_used=False, purchase_type=None, purchase_id=None)
    gen_paths.save()
    return redirect("purchase", "purchase")
    
    
urlpatterns_views = [
]

def show_paths(request):
    return render(request, "show_paths.html")