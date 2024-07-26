# Generated by Django 5.0.4 on 2024-06-12 14:59

import django.db.models.deletion
import file_system.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('filesize', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('load_date', models.DateTimeField(auto_now_add=True)),
                ('last_download_date', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('filepath', models.FileField(blank=True, null=True, upload_to=file_system.models.user_directory_path)),
                ('external_download_link', models.UUIDField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Файловый обменник',
                'verbose_name_plural': 'Файловый обменник',
                'db_table': 'file_system_model',
            },
        ),
    ]