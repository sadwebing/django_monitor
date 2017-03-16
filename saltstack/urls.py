from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('^check_minion$', views.CheckMinion),
    url('^command$', views.command),
    url('^command/execute$', views.CommandExecute),
    url('^id$', views.id),
    url('^$', views.command),
]
