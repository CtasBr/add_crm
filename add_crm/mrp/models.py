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
    units = models.ForeignKey(to="Unit", on_delete=models.PROTECT)
    def __str__(self) -> str:
        return self.title

class Application(models.Model):
    class Meta:
        db_table = "Applications"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
    
    title = models.CharField(verbose_name="Название", max_length=300)
    purchase_topic = models.ForeignKey(to="Purchase_topic", on_delete=models.PROTECT)
    creator = models.ForeignKey(to=User, on_delete=models.PROTECT)
    status = models.ForeignKey(to="Status", on_delete=models.PROTECT)
    positions = models.ManyToManyField("Position", blank=True)
    def __str__(self) -> str:
        return self.title
    