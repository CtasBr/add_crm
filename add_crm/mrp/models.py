from django.contrib.auth.models import User
from django.db import models


class Purchase_topic(models.Model):
    title = models.CharField(verbose_name="Название", max_length=300)
    stage = models.IntegerField(verbose_name="Этап", blank=True)

    def __str__(self):
        return self.title


class Status(models.Model):
    title = models.CharField(verbose_name="Название", max_length=300)
    def __str__(self) -> str:
        return self.title


class Units(models.Model):
    title = models.CharField(verbose_name="Название", max_length=300)
    def __str__(self) -> str:
        return self.title

class Positions(models.Model):
    title = models.CharField(verbose_name="Название", max_length=300)
    quantity = models.FloatField(verbose_name="Количество")
    units = models.ForeignKey(to="Units", on_delete=models.PROTECT)
    def __str__(self) -> str:
        return self.title

class Application(models.Model):
    title = models.CharField(verbose_name="Название", max_length=300)
    purchase_topic = models.ForeignKey(to="Purchase_topic", on_delete=models.PROTECT)
    creator = models.ForeignKey(to=User, on_delete=models.PROTECT)
    status = models.ForeignKey(to="Status", on_delete=models.PROTECT)
    positions = models.ManyToManyField("Empl", blank=True)
    def __str__(self) -> str:
        return self.title
    