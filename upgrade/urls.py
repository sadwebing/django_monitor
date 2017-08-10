from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url('^operate$', views.Operate),
    url('^query_svn$', views.QuerySvnId),
    url('^update_svn$', views.UpdateSvnId),
    url('^get_hosts$', views.GetHosts),
    url('^operate_upgrade$', views.OperateUpgrade),
    url('^op_upgrade/deploy$', views.OpUpgradeDeploy),
    url('^op_history$', views.OpHistory),
    url('^op_history/Query$', views.OpHistoryQuery),

]
