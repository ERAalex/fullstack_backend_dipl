from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from file_system.views import (upload_file, download_file, change_file, get_all_users_files, get_specific_user_files,
                               generate_external_download_link, download_file_by_external_link, change_security_link,
                               get_user_files, delete_file,)

router = DefaultRouter()

urlpatterns = [

    path('get_all_users_files/', get_all_users_files, name='get_all_users_files'),
    path('get_user_files/', get_user_files, name='get_user_files'),
    path('get_specific_user_files/<int:user_id>/', get_specific_user_files, name='get_specific_user_files'),

    path('upload-file/', upload_file, name='upload_file'),
    path('download-file/<int:file_id>/', download_file, name='download_file'),
    path('change-file/<int:file_id>/', change_file, name='change_file'),
    path('delete-file/<int:file_id>/', delete_file, name='delete_file'),

    # URLS to download files, logic
    path('generate-external-link/<int:file_id>/', generate_external_download_link,
         name='generate-external-download-link'),
    path('download-external-link/', download_file_by_external_link, name='download-external-link'),
    path('change-security-link/<int:file_id>/', change_security_link, name='change_security_link'),

    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
