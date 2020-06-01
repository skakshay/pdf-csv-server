
import json
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from .services import *
from .forms import *


class GetValueView(TemplateView):
    """
    A class used to handle view for displaying the value of query 
    params and providing the feature to downaload the csv

    ...

    Attributes
    ----------
    template_name : str
        template to be loaded on get request
    
    Methods
    -------
    get_context_data(self, **kwargs)
        Adds additional context to be passed to the template
    """


    template_name = 'coreapp/result.html'

    def get_context_data(self, **kwargs):
        """Adds additional context to be passed to the template

        Parameters
        ----------
        **kwargs
            Additional keyord arguments

        Returns
        -------
        dict
            Dictionary with additional context
        """

        context = super().get_context_data(**kwargs)
        context['query_variable'] = self.request.session['query_variable']
        context['query_year'] = self.request.session['query_year']
        context['value'] = self.request.session['value']
        context['file_path'] = self.request.session['file_path']
        return context


class DataParsingView(FormView):

    """
    A class used to handle view handling the display and submission 
    of the form

    ...

    Attributes
    ----------
    template_name : str
        template to be loaded on get request
    form_class : forms.Form
        form class to be loaded
    success_url : str
        url to be redirected to on successfull submission
    
    Methods
    -------
    get_form_kwargs(self)
        Adds additional params in form kwargs
    """

    template_name = 'coreapp/index.html'
    form_class = SubmissionForm
    success_url = reverse_lazy('coreapp:get-value')

    def get_form_kwargs(self):
        """Adds additional context to be passed to the template
        """

        kwargs = super(DataParsingView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
