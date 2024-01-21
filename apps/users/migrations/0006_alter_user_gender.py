# Generated by Django 5.0 on 2024-01-19 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], db_default=models.Value('O'), default='O', max_length=10),
        ),
    ]
