# Generated by Django 5.0 on 2024-02-05 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_super_admin',
            field=models.BooleanField(default=False),
        ),
    ]
