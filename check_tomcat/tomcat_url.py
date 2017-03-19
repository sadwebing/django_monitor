# coding: utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from models import tomcat_status,tomcat_url, tomcat_project
import json, logging
logger = logging.getLogger('django')

@csrf_exempt
def UrlQuery(request):
    if request.method == 'POST':
        return HttpResponse('You get nothing!')
    elif request.method == 'GET':
        clientip = request.META['REMOTE_ADDR']
        data = tomcat_url.objects.all()
        url_list = []
        logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
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
def UrlAdd(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        #data = json.loads(request.body)
        data = request.POST
        try:
            info = tomcat_url.objects.get(url=data['url'])
            logger.info('%s is requesting. %s url: %s  already exists!' %(clientip, request.get_full_path(), info.url))
            return HttpResponse('url: %s  already exists!' %info.url)
        except:
            logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))
            info = tomcat_url(project=data['project'], domain=data['domain'], url=data['url'], status=data['status_'])
            info.save()
            return HttpResponse('添加成功！')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt 
def UrlUpdate(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        #data = json.loads(request.body)
        data = request.POST
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))
        info = tomcat_url.objects.get(id=data['id'])
        info.project = data['project']
        info.domain  = data['domain']
        info.url     = data['url']
        info.status = data['status_']
        info.save()
        return HttpResponse('更新成功！')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt 
def UrlDelete(request):
    clientip = request.META['REMOTE_ADDR']
    logger.info('user: %s' %request.user.username)
    username = request.user.username
    if username != u'arno':
        logger.info('%s %s is requesting. %s' %(clientip, username, request.get_full_path()))
        return HttpResponse('你没有删除的权限，请联系管理员。')
    #data = json.loads(request.body)
    #logger.info('%s' %data)
    #return HttpResponse('success!')
    if request.method == 'POST':
        datas = json.loads(request.body)
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), datas))
        for data in datas:
        	info = tomcat_url.objects.get(id=data['id'],)
        	info.delete()
        return HttpResponse('删除成功！')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')