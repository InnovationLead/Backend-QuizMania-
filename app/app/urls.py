"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import View
from django.http import JsonResponse

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.urls import re_path


# status endpoint for health checks
class StatusView(View):
    def get(self,request,*args,**kwargs):
        return JsonResponse({"status": "ok"},status=200)



    
schema_view = get_schema_view(
    openapi.Info(
        title="QuizMania API",
        default_version="v1",
        description="This is QuizMania API docs.",
        terms_of_service="https://www.quizmania.com/policies/terms/",
        contact=openapi.Contact(email="contact@quizmania.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # A status endpoint for health check
    path('api/auth/',include('authentication.urls')),
    path('api/quiz/',include('quiz_app.urls')),
    path('status/',view=StatusView.as_view(),name='status'),
    path('admin/', admin.site.urls),
]
