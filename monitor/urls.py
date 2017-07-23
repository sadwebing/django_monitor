"""monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib import auth
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect

urlpatterns = [
    #url(r'^', include('clientservices.urls')),
    #url(r'^$', include('clientservices.urls')),
    url(r'^', include('check_tomcat.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^monitor_server/', include('check_tomcat.urls')),
    #url(r'^accounts/', include('accounts.urls')),
    url(r'^tomcat/', include('check_tomcat.urls')),
    url(r'^saltstack/', include('saltstack.urls')),
    url(r'^malfunction/', include('clientservices.urls')),
    url(r'^upgrade/', include('upgrade.urls')),
    url(r'^favicon$', lambda x: HttpResponseRedirect(settings.STATIC_URL+'images/favicon.ico')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
