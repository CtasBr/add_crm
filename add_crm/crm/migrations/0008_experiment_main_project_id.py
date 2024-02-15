# Generated by Django 5.0.2 on 2024-02-15 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0007_alter_variation_main_experiment_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="experiment",
            name="main_project_id",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.PROTECT, to="crm.project"
            ),
            preserve_default=False,
        ),
    ]
