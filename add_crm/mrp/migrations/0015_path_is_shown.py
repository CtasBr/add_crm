# Generated by Django 5.0.2 on 2024-09-11 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mrp", "0014_alter_application_creator_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="path",
            name="is_shown",
            field=models.BooleanField(default=False, verbose_name="показан"),
        ),
    ]
