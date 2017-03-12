from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url('^check/$', views.MonitorServer),
    url('index/$', views.index),
    url('project/$', views.project),
<<<<<<< HEAD
    url('tomcat_project/Query$', views.ProjectQuery),
    url('tomcat_project/Update$', views.ProjectUpdate),
    url('tomcat_project/Add$', views.ProjectAdd),
    url('tomcat_project/Delete$', views.ProjectDelete),
=======
    url('tomcat_project/query$', views.ProjectQuery),
>>>>>>> 9fc7d037d7bd5eadabf6a6ace93719a19384a120
    url('tomcat_url/$', views.TomcatUrl),
    url('Add$', views.Add),
    url('Update$', views.Update),
    url('^$', views.index),
    #url('favicon.ico',RedirectView.as_view(url='/static/images/favicon.ico')),
    #url(r'^favicon.ico$', lambda x: HttpResponseRedirect(settings.STATIC_URL+'images/favicon.ico')),
]
