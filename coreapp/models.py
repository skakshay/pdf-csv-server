from django.db import models

# Create your models here.


class File(models.Model):
    file = models.FileField(upload_to='excel/%Y/%m/%d/')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)



class BalanceSheet(models.Model):

    particular = models.CharField(db_index=True, max_length=128)
    value = models.FloatField()
    year = models.IntegerField(db_index=True)
    file = models.ForeignKey('File', on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('year', 'particular')
