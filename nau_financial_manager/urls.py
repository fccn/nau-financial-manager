"""
URL configuration for nau_financial_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title=settings.SWAGGER_PROJECT_NAME,
        default_version=settings.SWAGGER_PROJECT_VERSION,
        description=settings.SWAGGER_DESCRIPTION,
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/redocs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api-auth/", include("rest_framework.urls")),
]

urlpatterns += [
    # CUSTOM APPS
    path("api/billing/", include("apps.billing.urls")),
    path("api/organization/", include("apps.organization.urls")),
    path("api/shared-revenue/", include("apps.shared_revenue.urls")),
]

# Optionally deliver static assets by the application.
if getattr(settings, "STATIC_FILES_URL_ENABLE", False) or settings.DEBUG:
    urlpatterns = staticfiles_urlpatterns() + urlpatterns
