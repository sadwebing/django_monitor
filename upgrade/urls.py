from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url('^operate$', views.Operate),
    url('^query_svn$', views.QuerySvnId),
    url('^operate_upgrade$', views.OperateUpgrade),
]
