# Generated by Django 5.0.2 on 2024-06-20 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mrp", "0011_equipment_quantity_equipmentapplication"),
    ]

    operations = [
        migrations.AddField(
            model_name="equipment",
            name="link",
            field=models.CharField(
                default="link", max_length=1000, verbose_name="Ссылка"
            ),
            preserve_default=False,
        ),
    ]