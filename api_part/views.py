
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AdminUserSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework_simplejwt.tokens import RefreshToken


class CreateAdminUserView(APIView):
    """
    Create a new admin user
    temporary decision for testing
    """

    def post(self, request):
        try:
            serializer = AdminUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def list_users(request):
    users = User.objects.all().values('id', 'username', 'email', 'is_staff')
    users_list = list(users)
    return Response(users_list)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_user(request):
    """
    Create a new user
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    """
    Delete a user by ID
    """
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({"ok": "User deleted"}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def change_user_status(request, user_id):
    """
    Set or unset a user as admin based on the is_admin parameter.
    """
    try:
        # Fetch the user by user_id
        user = User.objects.get(pk=user_id)

        if user.is_staff:
            user.is_staff = False
        else:
            user.is_staff = True

        # Update the user's is_staff status
        user.save()

        # Prepare the response message
        status_message = f"User set {user.is_staff}."
        return Response({"message": status_message, "user_id": user.id, "is_staff": user.is_staff},
                        status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def data_user(request, user_id):
    """
    Retrieve user information by user ID
    """

    # Check if the requesting user is an admin or the user themselves
    if not request.user.is_superuser and request.user.id != user_id:
        return Response({"error": "You do not have permission to access this information"}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user_info = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_superuser,
    }

    return Response(user_info, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def personal_info(request):
    """
    Retrieve user information by user ID
    """

    print(request.user)
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user_info = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_superuser,
    }

    return Response(user_info, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Log out all user.
    Args:
        request (HttpRequest): The client's request to the server.
    Returns:
        HttpResponseRedirect: Redirects the user to the Login page.
    """

    if request.method == 'POST':
        try:
            # Extract access token from Authorization header
            refresh_token = request.data["refresh"]

            # Blacklist the refresh token
            refresh_token_obj = RefreshToken(refresh_token)
            refresh_token_obj.blacklist()

            return Response({'message': 'User logout successfully'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
