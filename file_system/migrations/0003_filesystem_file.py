# Generated by Django 5.0.4 on 2024-08-02 21:02

import file_system.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_system', '0002_remove_filesystem_filepath'),
    ]

    operations = [
        migrations.AddField(
            model_name='filesystem',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=file_system.models.user_directory_path),
        ),
    ]
