from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from file_system.views import upload_file, get_user_files, get_specific_user_files


urlpatterns = [
    path('upload-file/', upload_file, name='upload_file'),
    path('get_user_files/', get_user_files, name='get_user_files'),
    path('get_user_files/<int:user_id>/', get_specific_user_files, name='get_specific_user_files'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
