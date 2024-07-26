from django.contrib import admin
from file_system.models import FileSystem


@admin.register(FileSystem)
class FileSystemAdmin(admin.ModelAdmin):
    list_display = ['user', 'filename',]
