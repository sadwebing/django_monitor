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
def ProjectQuery(request):
    clientip = request.META['REMOTE_ADDR']
    if request.method == 'POST':
        return HttpResponse('You get nothing!')
    elif request.method == 'GET':
        data = tomcat_project.objects.all()
        project_list = []
        logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
        for project in data:
            tmp_dict = {}
            tmp_dict['id'] = project.id
            tmp_dict['product'] = project.product
            tmp_dict['project'] = project.project
            tmp_dict['code_dir'] = project.code_dir
            tmp_dict['tomcat'] = project.tomcat
            tmp_dict['main_port'] = project.main_port
            tmp_dict['jdk'] = project.jdk
            tmp_dict['script'] = project.script
            tmp_dict['status_'] = project.status
            project_list.append(tmp_dict)
        return HttpResponse(json.dumps(project_list))
        #return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt 
def ProjectAdd(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        #data = json.loads(request.body)
        data = request.POST
        try:
            info = tomcat_project.objects.get(project=data['project'])
            return HttpResponse('PROJECT: %s  already exists!' %info.project)
        except:
            logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))
            if data['status_'] == '':
            	status_ = 'active'
            else:
            	status_ = data['status_']
            info = tomcat_project(product=data['product'], project=data['project'], code_dir=data['code_dir'], tomcat=data['tomcat'], main_port=data['main_port'], jdk=data['jdk'], script=data['script'], status=status_)
            info.save()
            return HttpResponse('添加成功！')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt 
def ProjectUpdate(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        #data = json.loads(request.body)
        data = request.POST
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))
        if data['status_'] == '':
        	status_ = 'inactive'
        else:
        	status_ = data['status_']
        info = tomcat_project.objects.get(id=data['id'])
        info.product   = data['product']
        info.project   = data['project']
        info.code_dir  = data['code_dir']
        info.tomcat    = data['tomcat']
        info.main_port = data['main_port']
        info.jdk       = data['jdk']
        info.script    = data['script']
        info.status    = status_
        info.save()
        return HttpResponse('success!')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt 
def ProjectDelete(request):
    clientip = request.META['REMOTE_ADDR']
    #data = json.loads(request.body)
    #logger.info('%s' %data)
    #return HttpResponse('success!')
    username = request.user.username
    if username != u'arno':
        return HttpResponse('你没有删除的权限，请联系管理员。')
    if request.method == 'POST':
        datas = json.loads(request.body)
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), datas))
        for data in datas:
        	info = tomcat_project.objects.get(id=data['id'],)
        	info.delete()
        return HttpResponse('删除成功！')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')