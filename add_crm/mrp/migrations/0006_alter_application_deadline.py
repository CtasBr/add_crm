# Generated by Django 5.0.2 on 2024-06-04 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mrp", "0005_application_deadline"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="deadline",
            field=models.DateField(blank=True, verbose_name="Срок поставки"),
        ),
    ]
