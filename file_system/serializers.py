from django.contrib.auth.models import User
from rest_framework import serializers
from .models import FileSystem


class FileSystemSerializers(serializers.ModelSerializer):
    class Meta:
        model = FileSystem
        fields = "__all__"


class UpdateFileSystemSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FileSystem
        fields = ['filename', 'comment', 'user']
