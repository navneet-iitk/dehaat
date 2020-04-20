from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from . import serializers as balance_sheet_serializers
from dehaat.balance_sheet import models as balance_sheet_models


class BalanceSheetViewset(GenericViewSet):

    serializer_class = balance_sheet_serializers.BalanceSheetUploadSerializer

    def get_queryset(self):
        return balance_sheet_models.BalanceSheet.objects.all()

    def parse(self, request):
        serializer = balance_sheet_serializers.BalanceSheetUploadSerializer(data=request.data, context={})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        pdf_file = data['balance_sheet']
        csv_data = data['csv_data']
        csv_file_name = data['csv_file_name']
        query_variable = data.get('query_variable')
        query_year = data.get('query_year')
        query_value = data.get('value')
        try:
            balance_sheet_obj = balance_sheet_models.BalanceSheet(balance_sheet=pdf_file,
                                                                  query_variable=query_variable,
                                                                  query_year=query_year,
                                                                  query_value=query_value,
                                                                  )
            balance_sheet_obj.csv_file.save(name=csv_file_name, content=csv_data, save=True)
            obj_data = balance_sheet_serializers.BalanceSheetModelSerializer(balance_sheet_obj).data
        except Exception as e:
            return Response({'status': 0, 'error': str(e), 'message': 'Failed to upload balance sheet'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return render(request, 'download_balance_sheet_csv.html', context={**obj_data})


    def list(self, request):
        objs = balance_sheet_models.BalanceSheet.objects.all()
        data = balance_sheet_serializers.BalanceSheetModelSerializer(objs, many=True).data
        return Response(data)