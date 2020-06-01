from django.db import models

# Create your models here.


class File(models.Model):
    """
    A class used to handle model for holding the converted csv file

    ...

    Attributes
    ----------
    file : FileField
        file uploaded
    created_date : DateTimeField
        creation time
    modified_date : DateTimeField
        last modification time
    """

    file = models.FileField(upload_to='excel/%Y/%m/%d/')      # Saves the uploaded files in {MEDIA_ROOT}/excel/%Y/%m/%d/ directory
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)



class BalanceSheet(models.Model):
    """
    A class used to handle model for holding the data of converted csv file

    ...

    Attributes
    ----------
    particular : CharFeeld
        name of particular
    value : FloatField
        value of particular
    year : IntegertField
        year
    file : ForeignKey
        reference of File model
    created_date : DateTimeField
        creation time
    modified_date : DateTimeField
        last modification time
    """

    particular = models.CharField(db_index=True, max_length=128)
    value = models.FloatField()
    year = models.IntegerField(db_index=True)
    file = models.ForeignKey('File', on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        """    
        An inner class used to add additional uniqueness constraint

        ...

        Attributes
        ----------
        unique_together : tuple
            columns which need to be unique in combination
        """
        
        unique_together = ('year', 'particular')        # particular and year combined together must be unique
