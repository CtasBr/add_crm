# Generated by Django 5.0.2 on 2024-02-15 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0005_rename_done_subtask_is_done"),
    ]

    operations = [
        migrations.AddField(
            model_name="variation",
            name="main_experiment_id",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.PROTECT, to="crm.project"
            ),
            preserve_default=False,
        ),
    ]
