from django.core.exceptions import ValidationError
import datetime

def validate_year(value):
    """Validates a string to be a valid year

        Parameters
        ----------
        value: str
            the value to be validated

        Raises
        ------
        ValidationError
            If the value passed is not a valid year
        """
    if value.isdigit() and int(value)>datetime.datetime.now().year:
        raise ValidationError("Please enter a valid query year")
