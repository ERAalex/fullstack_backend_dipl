from django.db import models
from django.contrib.auth.models import User
from backend_cloud_dipl.settings import BASE_MEDIA_DIR


def user_directory_path(instance, filename):
    return '{0}/{1}/{2}'.format(BASE_MEDIA_DIR, instance.user.id, filename)


class FileSystem(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    filesize = models.PositiveIntegerField(editable=False, null=True, blank=True)
    load_date = models.DateTimeField(auto_now_add=True)
    last_download_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    filepath = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    external_download_link = models.UUIDField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.filesize = self.filepath.size
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