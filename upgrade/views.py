# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from monitor import settings
#from check_tomcat.models import tomcat_project, tomcat_url
from models import upgrade_op, upgrade_cur_svn, svn_id
from check_tomcat.models import tomcat_project
from saltstack.saltapi import SaltAPI
import json, logging, numpy
from time import sleep
from dwebsocket import require_websocket
logger = logging.getLogger('django')
       
@csrf_exempt
@require_websocket
def OperateUpgrade(request):
    if request.is_websocket():
        logger.info(dir(request.websocket))
        #message = request.websocket.wait()
        for count in numpy.arange(1, 6):
            if count != 1:
                sleep(2)
            message_dict = {}
            message_dict['count'] = count
            message = "progessing step %s ......" %count
            message_dict['message'] = message
            logger.info(message_dict)
            request.websocket.send(json.dumps(message_dict))
            if count == 5:
                request.websocket.close()

@csrf_protect
@login_required
def Operate(request):
    global username, role, clientip
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    global clientip
    clientip = request.META['REMOTE_ADDR']
    title = u'升级-基本操作'
    logger.info('%s is requesting.' %clientip)
    return render(
        request,
        'upgrade/upgrade_operate.html',
        {
            'clientip':clientip,
            'title': title,
            'role': role,
            'username': username,
        }
    )


@csrf_exempt
def QuerySvnId(request):
    if request.method == 'GET':
        return HttpResponse('You get nothing!')
    elif request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        logger.info('[POST]%s is requesting. %s' %(clientip, request.get_full_path()))
        try:
            data = json.loads(request.body)
            act = data['act']
            #logger.info(data)
        except:
            act = 'null'
        if act == 'query_all':
            datas = svn_id.objects.all().order_by('-id')
        elif act == 'query_undone':
            datas = svn_id.objects.filter(status='undone').order_by('-id')
        elif act == 'query_done':
            datas = svn_id.objects.filter(status='done').order_by('-id')
        elif act == 'query_rollback':
            datas = svn_id.objects.filter(status='rollback').order_by('-id')
        else:
            return HttpResponse("参数错误！")
        logger.info('查询参数：%s' %act)
        svn_list = []
        for info in datas:
            tmp_dict = {}
            #select_id = tomcat_project.objects.filter(project=info.project).first()
            tmp_dict['id'] = info.id
            tmp_dict['svn_id'] = info.svn_id
            tmp_dict['id_time'] = info.id_time
            tmp_dict['tag'] = info.tag
            tmp_dict['project'] = info.project
            tmp_dict['cur_status'] = info.cur_status
            tmp_dict['info'] = info.info
            svn_list.append(tmp_dict)
        logger.info(svn_list)
        return HttpResponse(json.dumps(svn_list))
        #return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')