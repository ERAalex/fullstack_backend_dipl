# Generated by Django 5.0.4 on 2024-08-03 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_system', '0006_filesystem_filesize'),
    ]

    operations = [
        migrations.AddField(
            model_name='filesystem',
            name='total_downloads',
            field=models.IntegerField(default=0),
        ),
    ]
