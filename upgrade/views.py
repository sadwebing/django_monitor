# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from monitor import settings
from upgrade import Upgrade
#from check_tomcat.models import tomcat_project, tomcat_url
from models import upgrade_op, upgrade_cur_svn, svn_id, op_history
from check_tomcat.models import tomcat_project
from saltstack.saltapi import SaltAPI
import json, logging, numpy, datetime, requests
from time import sleep
from dwebsocket import require_websocket, accept_websocket
from accounts.limit import LimitAccess
from accounts.views import HasPermission
from edit_config import EditConfig

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
        LimitAccess(role, 'upgrade/upgrade_operate.html'),
        {
            'clientip':clientip,
            'title': title,
            'role': role,
            'username': username,
            'upgrade_api': settings.UPGRADE_API,
        }
    )

@csrf_protect
@login_required
def OpHistory(request):
    global username, role, clientip
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    global clientip
    clientip = request.META['REMOTE_ADDR']
    title = u'升级-操作记录'
    logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
    return render(
        request,
        LimitAccess(role, 'upgrade/op_history.html'),
        {
            'clientip':clientip,
            'title': title,
            'role': role,
            'username': username,
        }
    )

@csrf_exempt
def OpHistoryQuery(request):
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
            logger.info('null')
        if act == 'query_all':
            datas = op_history.objects.all().order_by('-id')[:data['limit']]
        else:
            return HttpResponse("参数错误！")
        logger.info('查询参数：%s' %act)
        svn_list = []
        for info in datas:
            tmp_dict = {}
            #select_id = tomcat_project.objects.filter(project=info.project).first()
            tmp_dict['id'] = info.id
            tmp_dict['svn_id'] = info.svn_id
            tmp_dict['project'] = info.project
            tmp_dict['ip_addr'] = info.ip_addr
            tmp_dict['act'] = info.act
            tmp_dict['op_time'] = info.op_time
            tmp_dict['com_time'] = info.com_time
            tmp_dict['op_user'] = info.op_user
            tmp_dict['op_ip_addr'] = info.op_ip_addr
            tmp_dict['op_status'] = info.op_status
            tmp_dict['backup_file'] = info.backup_file
            tmp_dict['envir'] = info.envir
            tmp_dict['info'] = info.info

            svn_list.append(tmp_dict)
        #logger.info(svn_list)
        return HttpResponse(json.dumps(svn_list))
        #return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

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

        if act == 'query_not_deleted':
            datas = svn_id.objects.filter(deleted=0).order_by('-id')
        elif act == 'query_deleted':
            datas = svn_id.objects.filter(deleted=1).order_by('-id')
        elif act == 'query_all':
            datas = svn_id.objects.all().order_by('-id')
        else:
            return HttpResponse("参数错误！")
        logger.info('查询参数：%s' %act)
        svn_list = []
        for info in datas:
            tmp_dict = {}
            #select_id = tomcat_project.objects.filter(project=info.project).first()
            try:
                postData = data['postData']
                if postData['project'] == 'all' and postData['cur_status_sel'] == 'all':
                    tmp_dict = getsvn(info)
                elif postData['project'] == 'all' and postData['cur_status_sel'] != 'all':
                    if info.envir_online in postData['cur_status_sel'] or info.envir_uat in postData['cur_status_sel']:
                        tmp_dict = getsvn(info)
                elif postData['project'] != 'all' and postData['cur_status_sel'] == 'all':
                    if info.project in postData['project']:
                        tmp_dict = getsvn(info)
                else:
                    if info.project in postData['project'] and (info.envir_online in postData['cur_status_sel'] or info.envir_uat in postData['cur_status_sel']):
                        tmp_dict = getsvn(info)
            except:
                tmp_dict = getsvn(info)
            if tmp_dict != {}:
                svn_list.append(tmp_dict)

        #logger.info(svn_list)
        return HttpResponse(json.dumps(svn_list))
        #return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

def getsvn(info):
    tmp_dict = {}
    tmp_dict['id'] = info.id
    tmp_dict['svn_id'] = info.svn_id
    tmp_dict['id_time'] = info.id_time
    tmp_dict['tag'] = info.tag
    tmp_dict['project'] = info.project
    tmp_dict['deleted'] = info.deleted
    tmp_dict['envir_uat'] = info.envir_uat
    tmp_dict['envir_online'] = info.envir_online
    tmp_dict['info'] = info.info
    return tmp_dict

@csrf_exempt
def UpdateSvnId(request):
    if request.method == 'GET':
        return HttpResponse('You get nothing!')
    elif request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        logger.info('[POST]%s is requesting. %s' %(clientip, request.get_full_path()))
        try:
            data = json.loads(request.body)
        except:
            return HttpResponse('failure')
        if data['act'] == 'update_deleted':
            if not HasPermission(request.user, 'change', 'svn_id', 'upgrade'):
                return HttpResponseForbidden('你没有修改的权限。')
            deleted = data['deleted']
            delete = svn_id.objects.get(id=data['id'])
            delete.deleted = deleted
            delete.save()
            logger.info('%s deleted %s success!' %(data['svn_id'], deleted))
        elif data['act'] == 'update_upgrade_status':
            update = svn_id.objects.get(id=data['id'])
            update.envir_uat = data['envir_uat']
            update.envir_online = data['envir_online']
            update.save()
            logger.info('update success: %s' %data)
        else:
            return HttpResponseServerError('执行动作错误，请检查！')
        return HttpResponse('success')
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def GetHosts(request):
    if request.method == 'POST':
        username = request.user.username
        try:
            role = request.user.userprofile.role
        except:
            role = 'none'
        clientip = request.META['REMOTE_ADDR']
        data = json.loads(request.body)
        logger.info('[POST]%s is requesting. %s : project %s' %(clientip, request.get_full_path(), data['project'][0]))
        exe = Upgrade(data, username, clientip)
        if exe:
            return HttpResponse(json.dumps(exe.getHosts()))
        else:
            return HttpResponseServerError('传入参数不是字典，请检查！')
    else:
        return HttpResponseForbidden('nothing!')

@require_websocket
@csrf_exempt
def OpUpgradeDeploy(request):
    if request.is_websocket():
        username = request.user.username
        try:
            role = request.user.userprofile.role
        except:
            role = 'none'
        clientip = request.META['REMOTE_ADDR']
        for postdata in request.websocket:
            if postdata:
                data = json.loads(postdata)

            logger.info('%s is requesting. %s 执行参数：%s' %(clientip, request.get_full_path(), data))
            #request.websocket.send(json.dumps(data))

            exe = Upgrade(data, username, clientip)
            if exe:
                request.websocket.send(json.dumps(exe.Execute()))
            else:
                data['op_status'] = -1
                data['result']    = 'none'
                request.websocket.send(json.dumps(data))
            continue