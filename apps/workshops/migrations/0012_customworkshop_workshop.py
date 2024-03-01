# Generated by Django 5.0 on 2024-02-18 20:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0011_remove_customworkshop_workshop_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='customworkshop',
            name='workshop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customizes', to='workshops.workshop'),
        ),
    ]
