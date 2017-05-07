from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url('^$', views.MalfunctionIndex),
    url('Query$', views.MalfunctionQuery),
    url('Update$', views.MalfunctionUpdate),
    url('Add$', views.MalfunctionAdd),
    url('Delete$', views.MalfunctionDelete),
    url('done$', views.MalfunctionDone),
    url('op_history$', views.OpHistory),
    url('QueryOpHistory$', views.QueryOpHistory),
]
