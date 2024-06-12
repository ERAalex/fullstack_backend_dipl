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
from django.utils import timezone

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


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_file(request, file_id):
    """
    Delete a file by its ID
    """

    try:
        file_instance = FileSystem.objects.get(id=file_id)
        # Check if the user is the owner of the file or an admin
        if request.user.id != file_instance.user.id and not request.user.is_superuser:
            return Response({"error": "You do not have permission to delete this file"}, status=status.HTTP_403_FORBIDDEN)

    except FileSystem.DoesNotExist:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

    file_instance.delete()
    return Response({"message": "File deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


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
        try:
            instance = self.get_object()
            instance.last_download_date = datetime.now()
            instance.save()

            file_handle = instance.filepath.open()
        except Exception as e:
            print(e)

        return FileResponse(file_handle, filename=instance.filepath.name, as_attachment=True)


class GenerateExternalDownloadLinkView(mixins.RetrieveModelMixin,
                                       GenericViewSet):
    queryset = FileSystem.objects.all()
    serializer_class = FileSystemSerializers
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        print('----get---file-link---')
        instance = self.get_object()

        external_download_uuid = uuid.uuid3(uuid.NAMESPACE_URL, str(instance.filepath))
        instance.external_download_link = external_download_uuid
        instance.save()

        download_link = 'files/download_external_link?uuid='
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
