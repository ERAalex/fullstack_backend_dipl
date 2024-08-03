from functools import wraps
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import FileSystem


def user_or_admin_required(func):
    """
    Decorator to check if the request user is either an admin or the owner of the file.
    """
    @wraps(func)
    def _wrapped_view(request, file_id, *args, **kwargs):
        # Get the file instance
        instance = get_object_or_404(FileSystem, id=file_id)

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

        # Check if user is admin or the file belongs to the user
        is_admin = request.user.is_superuser
        user_id = request.user.id
        file_owner_id = instance.user.id

        if not is_admin and user_id != file_owner_id:
            return JsonResponse({'detail': 'You do not have permission to access this file.'}, status=403)

        # Proceed with the view function if the check passes
        return func(request, file_id, *args, **kwargs)

    return _wrapped_view
