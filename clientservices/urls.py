from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
	url('^$', views.MalfunctionAll),
    url('all$', views.MalfunctionAll),
    url('undone$', views.MalfunctionIndex),
    url('done$', views.MalfunctionDone),
    url('QueryAll$', views.MalfunctionQueryAll),
    url('Query$', views.MalfunctionQuery),
    url('Update$', views.MalfunctionUpdate),
    url('Add$', views.MalfunctionAdd),
    url('Delete$', views.MalfunctionDelete),
    url('op_history$', views.OpHistory),
    url('QueryOpHistory$', views.QueryOpHistory),
    url('angular$', views.angular),
    url('PageTab$', views.PageTab),
    url('Page1$', views.Page1),
    url('Page2$', views.Page2),
]
