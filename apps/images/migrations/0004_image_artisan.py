# Generated by Django 5.0 on 2024-01-29 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artisans', '0001_initial'),
        ('images', '0003_image_blurhash_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='artisan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='artisans.artisan'),
        ),
    ]
