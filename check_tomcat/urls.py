from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url('^check/$', views.MonitorServer),
    url('index/$', views.index),
    url('project/$', views.project),
    url('tomcat_url/$', views.TomcatUrl),
    url('Add$', views.Add),
    url('Update$', views.Update),
    url('^$', views.index),
    #url('favicon.ico',RedirectView.as_view(url='/static/images/favicon.ico')),
    #url(r'^favicon.ico$', lambda x: HttpResponseRedirect(settings.STATIC_URL+'images/favicon.ico')),
]
