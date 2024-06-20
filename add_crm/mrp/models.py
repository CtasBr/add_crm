import datetime

from django.contrib.auth.models import User
from django.db import models


class Purchase_topic(models.Model):
    class Meta:
        db_table = "Purchase topics"
        verbose_name = "Тема закупок"
        verbose_name_plural = "Темы закупок"
        
    title = models.CharField(verbose_name="Название", max_length=300)
    stage = models.IntegerField(verbose_name="Этап", blank=True)

    def __str__(self):
        return self.title


class Status(models.Model):
    class Meta:
        db_table = "Statuses"
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
    
    title = models.CharField(verbose_name="Название", max_length=300)
    def __str__(self) -> str:
        return self.title


class Unit(models.Model):
    class Meta:
        db_table = "Units"
        verbose_name = "Единица измерений"
        verbose_name_plural = "Единицы измерений"
    
    title = models.CharField(verbose_name="Название", max_length=300)
    def __str__(self) -> str:
        return self.title

class Position(models.Model):
    class Meta:
        db_table = "Positions"
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"
    
    title = models.CharField(verbose_name="Название", max_length=300)
    quantity = models.FloatField(verbose_name="Количество")
    units = models.ForeignKey(verbose_name="Единица измерения", to="Unit", on_delete=models.PROTECT)
    link = models.ManyToManyField("Link", blank=True, verbose_name="Сслыки")
    min_quantity = models.FloatField(verbose_name="Минимальное количество", blank=True, null=True)
    is_done = models.BooleanField(verbose_name="Закуплена")
    def __str__(self) -> str:
        return self.title

class Application(models.Model):
    payment_forms = (
        ('Постоплата', 'Постоплата'),
        ('30/70', '30/70'),
    )
    class Meta:
        db_table = "Applications"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
    
    purchase_topic = models.ForeignKey(verbose_name="Тема закупки", to="Purchase_topic", on_delete=models.PROTECT)
    creator = models.ForeignKey(verbose_name="Создатель", to=User, on_delete=models.PROTECT)
    status = models.ForeignKey(verbose_name="Статус", to="Status", on_delete=models.PROTECT)
    payment_form = models.CharField(verbose_name="Оплата", choices=payment_forms, max_length=100)
    positions = models.ManyToManyField("PositionInApplication", blank=True, verbose_name="Позиции")
    provider = models.ForeignKey(to="Provider", verbose_name="Поставщик", on_delete=models.PROTECT)
    deadline = models.DateField(verbose_name="Срок поставки", blank=True, null=True)
    def __str__(self) -> str:
        return f'{self.provider.name} {self.purchase_topic}'
    
    
class TraceLogUnit(models.Model):
    class Meta:
        db_table = "TraceLogUnits"
        verbose_name = "Лог"
        verbose_name_plural = "Логи"
    
    user_name = models.ForeignKey(to=User, verbose_name="Пользователь", on_delete=models.PROTECT)
    object = models.ForeignKey(to=Position, verbose_name="Позиция", on_delete=models.PROTECT)
    count_units = models.FloatField()
    action = models.CharField(verbose_name="Действие", max_length=300)
    
    def __str__(self) -> str:
        return f'{self.user_name.first_name} {self.user_name.last_name} {self.action} {self.count_units} {self.object.units} {self.object}'
    

class Provider(models.Model):
    class Meta:
        db_table = "Providers"
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
    
    name = models.CharField(verbose_name="Название", max_length=300, blank=True)
    link = models.CharField(verbose_name="Ссылка", max_length=1000)
    
    def __str__(self) -> str:
        return self.name


class Link(models.Model):
    class Meta:
        db_table = "Links"
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"
    
    link = models.CharField(verbose_name="Ссылка", max_length=1000)
    appl = models.ForeignKey(to="Application", verbose_name="Для заявки", on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return self.link


class PositionInApplication(models.Model):
    class Meta:
        db_table = "PositionsInApplication"
        verbose_name = "Позиция в заявке"
        verbose_name_plural = "Позиции в заявке"
    
    position = models.ForeignKey(to="Position", verbose_name="Позиция", on_delete=models.PROTECT)
    quantity = models.FloatField(verbose_name="Количество")
    units = models.ForeignKey(verbose_name="Единица измерения", to="Unit", on_delete=models.PROTECT)
    link = models.CharField(verbose_name="Ссылка", max_length=1000)
    
    def __str__(self) -> str:
        return f'{self.position.title} {self.quantity} {self.units}'
    
class ApplicationTechnicalSpecification(models.Model):
    payment_forms = (
        ('Постоплата', 'Постоплата'),
        ('30/70', '30/70'),
    )
    class Meta:
        db_table = "ApplicationTechnicalSpecifications"
        verbose_name = "Заявка с ТЗ"
        verbose_name_plural = "Заявки с ТЗ"
    
    purchase_topic = models.ForeignKey(verbose_name="Тема закупки", to="Purchase_topic", on_delete=models.PROTECT)
    creator = models.ForeignKey(verbose_name="Создатель", to=User, on_delete=models.PROTECT)
    status = models.ForeignKey(verbose_name="Статус", to="Status", on_delete=models.PROTECT)
    payment_form = models.CharField(verbose_name="Оплата", choices=payment_forms, max_length=100)
    technical_specification = models.FileField(verbose_name="Файл", upload_to='technical_specification/', blank=True, null=True)
    file_name = models.CharField(verbose_name="Имя файла", max_length=100, blank=True, null=True)
    provider = models.ForeignKey(to="Provider", verbose_name="Поставщик", on_delete=models.PROTECT)
    deadline = models.DateField(verbose_name="Срок поставки", blank=True, null=True)
    
    def __str__(self) -> str:
        return self.provider.name
    

class Equipment(models.Model):
    class Meta:
        db_table = "Equipments"
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
    
    name = models.CharField(verbose_name="Название", max_length=1000)
    quantity = models.IntegerField(verbose_name="Количество")
    link = models.CharField(verbose_name="Ссылка", max_length=1000)
    
    def __str__(self) -> str:
        return self.name
    

class EquipmentApplication(models.Model):
    payment_forms = (
        ('Постоплата', 'Постоплата'),
        ('30/70', '30/70'),
    )
    class Meta:
        db_table = "EquipmentApplications"
        verbose_name = "Заявка на оборудование"
        verbose_name_plural = "Заявки на оборудование"
    
    purchase_topic = models.ForeignKey(verbose_name="Тема закупки", to="Purchase_topic", on_delete=models.PROTECT)
    creator = models.ForeignKey(verbose_name="Создатель", to=User, on_delete=models.PROTECT)
    status = models.ForeignKey(verbose_name="Статус", to="Status", on_delete=models.PROTECT)
    payment_form = models.CharField(verbose_name="Оплата", choices=payment_forms, max_length=100)
    provider = models.ForeignKey(to="Provider", verbose_name="Поставщик", on_delete=models.PROTECT)
    deadline = models.DateField(verbose_name="Срок поставки", blank=True, null=True)
    equipment = models.ManyToManyField("Equipment", blank=True, verbose_name="Оборудование")
    
    def __str__(self) -> str:
        return f'{self.purchase_topic.title} {self.provider.name}'