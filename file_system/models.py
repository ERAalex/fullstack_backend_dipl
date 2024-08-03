from django.db import models
from django.contrib.auth.models import User
from backend_cloud_dipl.settings import BASE_MEDIA_DIR
import os


def user_directory_path(instance, filename):
    return '{0}/{1}/{2}'.format(BASE_MEDIA_DIR, instance.user.id, filename)


class FileSystem(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=255, null=True, blank=True)
    filesize = models.CharField(max_length=10, editable=False, null=True, blank=True)
    load_date = models.DateTimeField(auto_now_add=True)
    last_download_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    external_download_link = models.UUIDField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically set file_type based on the filename
        if self.file:
            _, file_extension = os.path.splitext(self.file.name)
            self.file_type = file_extension.lower().replace('.', '')

        # Convert filesize to MB and format to 2 decimal places (in case if file less than 1 mb)
        self.filesize = round(self.file.size / (1024 * 1024), 2)
        super(FileSystem, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.filename

    class Meta:
        verbose_name = 'Файловый обменник'
        verbose_name_plural = 'Файловый обменник'
        db_table = "file_system_model"


    @classmethod
    def get_users_files(cls):
        pass

    @classmethod
    def get_file_path(cls, instance):
        return f'{BASE_MEDIA_DIR}/{instance.user.id}/{instance.filename}'
