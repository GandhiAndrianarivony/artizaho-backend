# Generated by Django 5.0 on 2024-02-07 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0008_remove_workshopbookable_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopbookable',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='workshopbookable',
            name='start_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='workshopbookable',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]