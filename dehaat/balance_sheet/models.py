from django.db import models
from config.storage_backends import PrivateMediaStorage
from django.core.validators import FileExtensionValidator


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BalanceSheet(TimeStampedModel):
    PDF_STORAGE_DIRECTORY = 'balance_sheets/pdfs'
    CSV_STORAGE_DIRECTORY = 'balance_sheets/csv'
    balance_sheet = models.FileField(upload_to='balance_sheets/pdfs',
                                     storage=PrivateMediaStorage(),
                                     validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    csv_file = models.FileField(upload_to=CSV_STORAGE_DIRECTORY,
                                storage=PrivateMediaStorage(),
                                validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    query_variable = models.CharField(max_length=64, null=True, blank=True)
    query_year = models.PositiveIntegerField(null=True, blank=True)
    query_value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'balance_sheet'
