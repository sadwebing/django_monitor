# coding: utf8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from dwebsocket import require_websocket
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from models import mail
import json, logging, requests, re, datetime
logger = logging.getLogger('django')
error_status = 'null'

@csrf_exempt
def MailQuery(request):
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
            datas = mail.objects.all()
        elif act == 'query_active':
            datas = mail.objects.filter(status='active')
        elif act == 'query_inactive':
            datas = mail.objects.filter(status='inactive')
        else:
            return HttpResponse("参数错误！")
        logger.info('查询参数：%s' %act)
        mail_list = []
        for mail_info in datas:
            tmp_dict = {}
            tmp_dict['id'] = mail_info.id
            tmp_dict['name'] = mail_info.name
            tmp_dict['mail_address'] = mail_info.mail_address
            tmp_dict['role'] = mail_info.role
            tmp_dict['check_services'] = mail_info.check_services
            tmp_dict['check_salt_minion'] = mail_info.check_salt_minion
            mail_list.append(tmp_dict)
        return HttpResponse(json.dumps(mail_list))
        #return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt 
def UpdateMailStatus(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        data = json.loads(request.body)
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))
        info = mail.objects.get(id=data['id'])
        if data['program'] == 'check_services':
            info.check_services = data[data['program']]
        elif data['program'] == 'check_salt_minion':
            info.check_salt_minion = data[data['program']]
            logger.info('check_salt_minion')
        else:
            logger.info('error')
            return HttpResponse('传入参数有误！')
        info.save()
        return HttpResponse('更新成功！')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')