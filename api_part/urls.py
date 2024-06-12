from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import CreateAdminUserView, list_users, create_user, delete_user

urlpatterns = [
    path('create-admin/', CreateAdminUserView.as_view(), name='create-admin'),
    path('create-user/', create_user, name='create_user'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('users/', list_users, name='list-users'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
