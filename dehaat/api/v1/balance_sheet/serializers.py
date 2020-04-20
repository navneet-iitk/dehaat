from rest_framework import serializers
import os
from django.core.files.base import ContentFile
from dehaat.balance_sheet import models as balance_sheet_models
from dehaat.api.v1 import utils as v1_utils


class BalanceSheetUploadSerializer(serializers.Serializer):

    #basic checks on the upload form input
    query_variable = serializers.CharField(max_length=64, allow_null=True, allow_blank=True, required=False)
    query_year = serializers.IntegerField(min_value=1, required=False, allow_null=True)
    balance_sheet = serializers.FileField()

    def validate(self, attrs):
        pdf_file = attrs['balance_sheet']
        query_variable = attrs.get('query_variable')
        query_year = attrs.get('query_year')

        # Condition to check if query_variable and query_year, either both of them are present or None is available.
        if bool(query_variable) ^ bool(query_year):
            raise serializers.ValidationError('Query variable are Query year both are required together')

        # File extension Check - Only PDFs are allowed
        if os.path.splitext(pdf_file.name)[1] != '.pdf':
            raise serializers.ValidationError('PDF file is required.')

        # extract dataframe for the table in the given PDF
        df = v1_utils.get_dataframe_from_pdf(pdf_file)

        # Raise bad request error if no dataframe found - i.e. no table, hence no balance sheet
        if df.empty:
            raise serializers.ValidationError('No table found in given balance sheet PDF')

        # extract the value for given query variable, if found value is added to attrs and query_variable is updated to display proper name
        if query_variable:
            query_variable, value = v1_utils.extract_data_from_dataframe(df, query_variable, query_year)
            if value:
                attrs['query_variable'] = query_variable
                attrs['value'] = value

        # removes empty columns and format the columm names
        df = v1_utils.clean_dataframe(df)

        csv_file_name = pdf_file.name.split('.')[0] + '.csv'
        csv_data = ContentFile(df.to_csv(index=False).encode())             # CSV data is transformed to raw content, encoded for hashing
        attrs['csv_data'] = csv_data
        attrs['csv_file_name'] = csv_file_name
        return attrs


class BalanceSheetModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = balance_sheet_models.BalanceSheet
        fields = ('id', 'balance_sheet', 'csv_file', 'query_variable', 'query_year', 'query_value')