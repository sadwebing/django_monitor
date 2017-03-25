from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('^check_minion$', views.CheckMinion),
    url('^command$', views.command),
    url('^restart$', views.restart),
    url('^restart/get_project$', views.GetProject),
    url('^command/execute$', views.CommandExecute),
    url('^command/restart$', views.CommandRestart),
    url('^saltstack_id$', views.Id),
    url('^saltstack_id/Query$', views.IdQuery),
    url('^saltstack_id/QueryMinion$', views.QueryMinion),
    url('^$', views.command),
]
