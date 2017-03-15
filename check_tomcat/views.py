# coding: utf8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from models import tomcat_status,tomcat_url, tomcat_project
import json, logging
from tomcat_project import *
from tomcat_url import *

logger = logging.getLogger('django')

@csrf_exempt 
def MonitorServer(request):
    if request.method == 'POST':
        ip = request.META['REMOTE_ADDR']
        clientip = request.META['REMOTE_ADDR']
        data = json.loads(request.body)
        #status = "\t".join([data['access_time'], data['project'], data['domain'], data['url'], data['code'], data['info']])
        logger.info('%s is requesting. %s' %(ip, data))
        status = tomcat_status(
            access_time = data['access_time'],
            project     = data['project'],
            domain      = data['domain'],
            url         = data['url'],
            code        = data['code'],
            info        = data['info'],
        )
        status.save()
        return HttpResponse("success!")
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_protect
@login_required
def index(request):
    title = u'管理中心'
    clientip = request.META['REMOTE_ADDR']
    logger.info('%s is requesting %s' %(clientip, request.get_full_path()))
    return render(
        request,
        'tomcat_index.html',
        {
            'title': title,
        }
    )
@csrf_protect
@login_required
def project(request):
    title = u'管理中心'
    clientip = request.META['REMOTE_ADDR']
    logger.info('%s is requesting %s' %(clientip, request.get_full_path()))
    return render(
        request,
        'tomcat_project.html',
        {
            'title': title,
        }
    )

