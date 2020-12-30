from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-token-auth/', obtain_jwt_token),
]
