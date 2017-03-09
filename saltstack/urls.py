from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('^check_minion$', views.CheckMinion),
    url('^index$', views.index),
]
