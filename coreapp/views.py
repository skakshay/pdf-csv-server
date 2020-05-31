
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
    template_name = 'coreapp/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query_variable'] = self.request.session['query_variable']
        context['query_year'] = self.request.session['query_year']
        context['value'] = self.request.session['value']
        context['file_path'] = self.request.session['file_path']
        return context


class DataParsingView(FormView):

    template_name = 'coreapp/index.html'
    form_class = SubmissionForm
    success_url = reverse_lazy('coreapp:get-value')

    def get_form_kwargs(self):
        kwargs = super(DataParsingView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
