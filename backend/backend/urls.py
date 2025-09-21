
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from library_api.lib.api.users import RegisterUserView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version="1.0.0",
        description="API Documentation of Library App"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[]
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/auth/register/", RegisterUserView.as_view(), name="register"),
    path('api/auth/login/', TokenObtainPairView.as_view(), name="login"),
    path('api/', include("library_api.urls")),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name="swagger-ui")
]
