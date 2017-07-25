from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url('index$', views.index),
    url('execute$', views.Execute),
]
