# Generated by Django 5.0 on 2024-03-10 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0018_workshopreservation_artisan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopreservation',
            name='custom_workshop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custom_workshop_booked', to='workshops.customworkshop'),
        ),
        migrations.AlterField(
            model_name='workshopreservation',
            name='workshop_bookable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workshop_booked', to='workshops.workshopbookable'),
        ),
    ]
