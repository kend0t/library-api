from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from library_api.lib.services.user_services import register_user
from library_api.lib.serializers.user_serializer import UserSerializer
from library_api.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user",
        responses={
            201: UserSerializer,
            400: "Username is already taken / Incomplete Data"
        }
    )
    def post(self, request):
        """Endpoint for registering a new account"""
        if User.objects.filter(username=request.data.get("username")).exists():
            return Response(
                {"message": "This username is already taken."},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = register_user(request.data)
        if not user:
            return Response({"message": "Data provided is invalid or incomplete"},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
