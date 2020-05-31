from django.core.exceptions import ValidationError
import datetime

def validate_year(value):
	if value.isdigit() and int(value)>datetime.datetime.now().year:
		raise ValidationError("Please enter a valid query year")
