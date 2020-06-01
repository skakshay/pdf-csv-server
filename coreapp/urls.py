

from django.contrib import admin
from django.urls import path, re_path
from coreapp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

app_name="coreapp"

urlpatterns = [
    path('uploadFile/', DataParsingView.as_view()),
    path('getValue/', GetValueView.as_view(), name='get-value')
] 