from library_api.models import User
from library_api.lib.serializers.user_serializer import UserSerializer


def register_user(user_data):
    """Register a new user"""
    serializer = UserSerializer(data=user_data)
    if serializer.is_valid():
        return serializer.save()
    return None
