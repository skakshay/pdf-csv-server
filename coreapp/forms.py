from django import forms
from .validators import *
from django.core.validators import FileExtensionValidator
from .services import *


class SubmissionForm(forms.Form):
    query_variable = forms.CharField(label='Query Variable', max_length=128, 
    	widget=forms.TextInput(attrs={'placeholder': 'NPA'}), 
    	error_messages={'required': 'Please enter the query variable', 'max_length':'Length of query variable exceeds max length'})

    query_year = forms.CharField(label='Query Year', max_length=4, 
    	widget=forms.TextInput(attrs={'placeholder': '2015'}), 
    	error_messages={'required': 'Please enter the relevant year', 'max_length':'Please enter a valid year'}, 
    	validators=[validate_year])

    pdf_file = forms.FileField(allow_empty_file=False, label='Please upload balance sheet', 
    	error_messages={'required': 'Please upload balance sheet', 'empty':'Please upload balance sheet'},
    	validators=[FileExtensionValidator(['pdf'])])

    def __init__(self, *args, **kwargs):
    	self.request = kwargs.pop('request')
    	super(SubmissionForm, self).__init__(*args, **kwargs)
    	


    def clean(self):
    	super().clean()
    	try:
    		convert_and_save_data(self.cleaned_data['pdf_file'])
    		query_variable = self.cleaned_data['query_variable']
    		query_year = self.cleaned_data['query_year']
    		value, file_path = get_value(query_variable, query_year)
    		self.request.session['value'] = value
    		self.request.session['file_path'] = file_path
    		self.request.session['query_year'] = query_year
    		self.request.session['query_variable'] = query_variable
    	except RuntimeError as re:
    		raise forms.ValidationError(str(re))
