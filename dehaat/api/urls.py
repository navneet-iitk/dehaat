from django.conf.urls import include
from django.urls import path

from .v1.balance_sheet.router import urlpatterns as balance_sheet_url

urlpatterns = [
    path('v1/balance_sheet/', include(balance_sheet_url)),
]