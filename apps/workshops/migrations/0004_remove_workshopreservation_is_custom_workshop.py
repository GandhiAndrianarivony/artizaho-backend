# Generated by Django 5.0 on 2024-02-01 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0003_customworkshop_workshop_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshopreservation',
            name='is_custom_workshop',
        ),
    ]
