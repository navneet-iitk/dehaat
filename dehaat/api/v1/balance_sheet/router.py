from django.urls import path
from .views import BalanceSheetViewset

# Balance Sheet API endpoints
urlpatterns = [
    path('parse', BalanceSheetViewset.as_view({'post':'parse'}), name='balance-sheet-parse'),       # API for parsing the PDF document to look out for query variable and CSV download
    # path('list', BalanceSheetViewset.as_view({'get':'list'}), name='balance-sheet-list'),         # API for listing all the uploaded balance sheets with their respextive queries and CSV files
]