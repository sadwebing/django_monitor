from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('^check_minion$', views.CheckMinion),
    url('^command$', views.command),
    url('^restart$', views.restart),
    url('^restart/get_project$', views.GetProject),
    url('^command/execute$', views.CommandExecute),
    url('^command/restart$', views.CommandRestart),
    url('^id$', views.id),
    url('^$', views.command),
]
