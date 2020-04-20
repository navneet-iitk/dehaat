from django.urls import path
from .views import BalanceSheetViewset


urlpatterns = [
    path('parse', BalanceSheetViewset.as_view({'post':'parse'}), name='balance-sheet-parse'),
    path('list', BalanceSheetViewset.as_view({'get':'list'}), name='balance-sheet-list'),
]