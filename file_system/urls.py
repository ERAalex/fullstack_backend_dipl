from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from file_system.views import (upload_file, rename_file, get_all_users_files, get_specific_user_files, get_user_files, delete_file,
                               DownloadFileView, GenerateExternalDownloadLinkView, ExternalDownloadLinkView)

router = DefaultRouter()
router.register(r'download_file', DownloadFileView, basename='download-file')
router.register(r'download_file_link', GenerateExternalDownloadLinkView, basename='download-file-link')

urlpatterns = [

    path('get_all_users_files/', get_all_users_files, name='get_all_users_files'),
    path('get_user_files/', get_user_files, name='get_user_files'),
    path('get_specific_user_files/<int:user_id>/', get_specific_user_files, name='get_specific_user_files'),

    path('upload-file/', upload_file, name='upload_file'),
    path('rename-file/<int:file_id>/', rename_file, name='rename_file'),
    path('delete-file/<int:file_id>/', delete_file, name='delete_file'),
    path('download_external_link', ExternalDownloadLinkView.as_view()),

    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
