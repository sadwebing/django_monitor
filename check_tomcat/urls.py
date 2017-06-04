from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url('^check/$', views.MonitorServer),
    url('tomcat_url$', views.tomcat_url),
    url('project/$', views.project),
    url('tomcat_project/Query$', views.ProjectQuery),
    url('tomcat_project/Update$', views.ProjectUpdate),
    url('tomcat_project/Add$', views.ProjectAdd),
    url('tomcat_project/Delete$', views.ProjectDelete),
    url('tomcat_url/Query$', views.UrlQuery),
    url('tomcat_url/Update$', views.UrlUpdate),
    url('tomcat_url/Add$', views.UrlAdd),
    url('tomcat_url/Delete$', views.UrlDelete),
    url('^tomcat_url/CheckServer$', views.UrlCheckServer),
    url('^$', views.index),
    #url('favicon.ico',RedirectView.as_view(url='/static/images/favicon.ico')),
    #url(r'^favicon.ico$', lambda x: HttpResponseRedirect(settings.STATIC_URL+'images/favicon.ico')),
]
