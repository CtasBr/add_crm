# Generated by Django 5.0.2 on 2024-06-19 13:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mrp", "0005_positioninapplication_units"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ApplicationTechnicalSpecification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "payment_form",
                    models.CharField(
                        choices=[("Постоплата", "Постоплата"), ("30/70", "30/70")],
                        max_length=100,
                        verbose_name="Оплата",
                    ),
                ),
                (
                    "technical_specification",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="technical_specification/",
                        verbose_name="Файл",
                    ),
                ),
                (
                    "deadline",
                    models.DateField(
                        blank=True, null=True, verbose_name="Срок поставки"
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Создатель",
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="mrp.provider",
                        verbose_name="Поставщик",
                    ),
                ),
                (
                    "purchase_topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="mrp.purchase_topic",
                        verbose_name="Тема закупки",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="mrp.status",
                        verbose_name="Статус",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заявка с ТЗ",
                "verbose_name_plural": "Заявки с ТЗ",
                "db_table": "ApplicationTechnicalSpecifications",
            },
        ),
    ]
