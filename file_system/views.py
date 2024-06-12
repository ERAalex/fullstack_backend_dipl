from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, status, parsers
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User

import os
import uuid
import pytz
from datetime import datetime

from .models import FileSystem
from .serializers import FileSystemSerializers, UpdateFileSystemSerializers


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    """
    Upload a new file
    """
    data_upload = request.data
    data_upload['user'] = request.user.id

    serializer = FileSystemSerializers(data=data_upload)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_files(request):
    """
    Get all users files
    """

    users_files = FileSystem.objects.filter(user=request.user)
    serializer = FileSystemSerializers(users_files, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_specific_user_files(request, user_id):
    """
    Get all files uploaded by a specific user
    """
    if request.user.id != user_id and not request.user.is_superuser:
        return Response({"error": "You cannot get this files"}, status=status.HTTP_404_NOT_FOUND)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user_files = FileSystem.objects.filter(user=user)
    serializer = FileSystemSerializers(user_files, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateFileSystemView(mixins.UpdateModelMixin,
                     GenericViewSet):
    queryset = FileSystem.objects.all()
    serializer_class = UpdateFileSystemSerializers
    permission_classes = [IsAuthenticated, IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.id != instance.user_id:
            raise AuthenticationFailed

        return super().update(request, *args, **kwargs)


class DownloadFileView(mixins.RetrieveModelMixin,
                       GenericViewSet):
    queryset = FileSystem.objects.all()
    serializer_class = FileSystemSerializers
    permission_classes = [IsAuthenticated, ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        tz_moskow = pytz.timezone(os.environ.get('TIMEZONE'))
        instance.last_download_date = datetime.now(tz_moskow)
        instance.save()

        file_handle = instance.filepath.open()
        return FileResponse(file_handle, filename=instance.filepath.name, as_attachment=True)


class GenerateExternalDownloadLinkView(mixins.RetrieveModelMixin,
                                       GenericViewSet):
    queryset = FileSystem.objects.all()
    serializer_class = FileSystemSerializers
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        external_download_uuid = uuid.uuid3(uuid.NAMESPACE_URL, str(instance.filepath))
        instance.external_download_link = external_download_uuid
        instance.save()

        download_link = 'api/v1/download_external_link?uuid='
        link_host = request.build_absolute_uri('/') + download_link
        external_download_link = f'{link_host}{external_download_uuid}'

        return Response({'link': external_download_link})


class ExternalDownloadLinkView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            get_uuid = request.query_params.get('uuid')
            queryset = FileSystem.objects.get(external_download_link=get_uuid)
        except ValidationError as E:
            return Response({
                'Error': E
            })

        file_handle = queryset.filepath.open()
        return FileResponse(file_handle, filename=queryset.filepath.name, as_attachment=True)
