from rest_framework import serializers
import os
from django.core.files.base import ContentFile
from dehaat.balance_sheet import models as balance_sheet_models
from dehaat.api.v1 import utils as v1_utils


class BalanceSheetUploadSerializer(serializers.Serializer):
    query_variable = serializers.CharField(max_length=64, allow_null=True, allow_blank=True, required=False)
    query_year = serializers.IntegerField(min_value=1, required=False, allow_null=True)
    balance_sheet = serializers.FileField()

    def validate(self, attrs):
        pdf_file = attrs['balance_sheet']
        query_variable = attrs.get('query_variable')
        query_year = attrs.get('query_year')
        if bool(query_variable) ^ bool(query_year):
            raise serializers.ValidationError('Query variable are Query year both are required together')
        if os.path.splitext(pdf_file.name)[1] != '.pdf':
            raise serializers.ValidationError('PDF file is required.')
        df = v1_utils.get_df_from_pdf(pdf_file)
        if df.empty:
            raise serializers.ValidationError('No table found in given balance sheet PDF')
        if query_variable:
            query_variable, value = v1_utils.extract_data_from_df(df, query_variable, query_year)
            if value:
                attrs['query_variable'] = query_variable
                attrs['value'] = value
        df = v1_utils.clean_df(df)
        csv_file_name = pdf_file.name.split('.')[0] + '.csv'
        csv_data = ContentFile(df.to_csv(index=False).encode())
        attrs['csv_data'] = csv_data
        attrs['csv_file_name'] = csv_file_name
        return attrs


class BalanceSheetModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = balance_sheet_models.BalanceSheet
        fields = ('id', 'balance_sheet', 'csv_file', 'query_variable', 'query_year', 'query_value')