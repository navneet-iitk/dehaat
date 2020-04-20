"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


additional_urls = [
    path('api/', include('dehaat.api.urls')),
    path('upload', TemplateView.as_view(template_name='upload_balance_sheet_pdf.html')),        # balance sheet upload input form
]

# if not API_ENABLED in env file, endpoints won't be available
if not settings.API_ENABLED:
    additional_urls = []

urlpatterns = [
    path('admin/', admin.site.urls),
] + additional_urls
