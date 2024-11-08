# Generated by Django 5.0.2 on 2024-11-02 10:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0016_result_is_shown_alter_subtask_is_done_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="result",
            name="main_task_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="results",
                to="crm.task",
            ),
        ),
    ]
