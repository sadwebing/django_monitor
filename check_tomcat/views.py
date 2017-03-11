# coding: utf8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from models import tomcat_status,tomcat_url
import json, logging

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

@csrf_exempt 
def TomcatUrl(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        data = tomcat_url.objects.all()
        url_list = []
        logger.info('%s is requesting. tomcat_url' %clientip)
        for url in data:
            tmp_dict = {}
            tmp_dict['id'] = url.id
            tmp_dict['project'] = url.project
            tmp_dict['domain'] = url.domain
            tmp_dict['url'] = url.url
            url_list.append(tmp_dict)
        return HttpResponse(url_list)
    elif request.method == 'GET':
        clientip = request.META['REMOTE_ADDR']
        data = tomcat_url.objects.all()
        url_list = []
        logger.info('%s is requesting. tomcat_url' %clientip)
        for url in data:
            tmp_dict = {}
            tmp_dict['id'] = url.id
            tmp_dict['project'] = url.project
            tmp_dict['domain'] = url.domain
            tmp_dict['url'] = url.url
            tmp_dict['status_'] = url.status
            url_list.append(tmp_dict)
        return HttpResponse(json.dumps(url_list))
        #return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt 
def Add(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        #data = json.loads(request.body)
        data = request.POST
        logger.info('%s' %data)
        info = tomcat_url(project=data['project'], domain=data['domain'], url=data['url'], status=data['status_'])
        info.save()
        return HttpResponse('success!')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt 
def Update(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        #data = json.loads(request.body)
        data = request.POST
        logger.info('%s' %data)
        info = tomcat_url.objects.get(id=data['id'])
        info.project = data['project']
        info.domain  = data['domain']
        info.url     = data['url']
        info.status = data['status_']
        info.save()
        return HttpResponse('success!')
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

