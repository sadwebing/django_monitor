# coding: utf8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json, logging
from models import malfunction 

logger = logging.getLogger('django')

@csrf_protect
@login_required
def MalfunctionIndex(request):
    title = u'管理中心-故障登记'
    global username, role
    username = request.user.username
    clientip = request.META['REMOTE_ADDR']
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    #logger.info(dir(request.user))
    #logger.info(request.user.userprofile.role)
    logger.info('%s is requesting %s' %(clientip, request.get_full_path()))
    return render(
        request,
        'malfunction/malfunction.html',
        {
            'title': title,
            'role': role,
            'username': username,
        }
    )

@csrf_protect
@login_required
def MalfunctionDone(request):
    title = u'管理中心-故障登记'
    clientip = request.META['REMOTE_ADDR']
    #logger.info(dir(request.user))
    #logger.info(request.user.userprofile.role)
    logger.info('%s is requesting %s' %(clientip, request.get_full_path()))
    return render(
        request,
        'malfunction/malfunction_done.html',
        {
            'title': title,
            'role': role,
            'username': username,
        }
    )

@csrf_exempt
def MalfunctionQuery(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        #datas = malfunction.objects.all()
        datas = malfunction.objects.filter(mal_status='已处理').order_by('-id')
        malfunction_list = []
        logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
        for data in datas:
            tmp_dict = {}
            tmp_dict['id'] = data.id
            tmp_dict['record_time'] = data.record_time
            tmp_dict['mal_details'] = data.mal_details
            tmp_dict['record_user'] = data.record_user
            tmp_dict['mal_reasons'] = data.mal_reasons
            tmp_dict['mal_status'] = data.mal_status
            tmp_dict['recovery_time'] = data.recovery_time
            tmp_dict['time_all'] = data.time_all
            tmp_dict['handle_user'] = data.handle_user
            malfunction_list.append(tmp_dict)
        return HttpResponse(json.dumps(malfunction_list))
    elif request.method == 'GET':
        clientip = request.META['REMOTE_ADDR']
        #datas = malfunction.objects.all()
        datas = malfunction.objects.filter(mal_status='未处理').order_by('-id')
        malfunction_list = []
        logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
        for data in datas:
            tmp_dict = {}
            tmp_dict['id'] = data.id
            tmp_dict['record_time'] = data.record_time
            tmp_dict['mal_details'] = data.mal_details
            tmp_dict['record_user'] = data.record_user
            tmp_dict['mal_reasons'] = data.mal_reasons
            tmp_dict['mal_status'] = data.mal_status
            tmp_dict['recovery_time'] = data.recovery_time
            tmp_dict['time_all'] = data.time_all
            tmp_dict['handle_user'] = data.handle_user
            malfunction_list.append(tmp_dict)
        return HttpResponse(json.dumps(malfunction_list))
        #return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def MalfunctionAdd(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        #data = json.loads(request.body)
        role = request.user.userprofile.role
        data = request.POST
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))
        info = malfunction(
        record_time = data['record_time'],
        mal_details = data['mal_details'],
        record_user = data['record_user'],
        #mal_reasons = data['mal_reasons'],
        #mal_status  = data['mal_status'],
        #recovery_time = data['recovery_time'],
        #time_all = data['time_all'],
        #handle_user = data['handle_user'],
        )
        info.save()
        return HttpResponse('新增成功！')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def MalfunctionUpdate(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        #data = json.loads(request.body)
        role = request.user.userprofile.role
        data = request.POST
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))
        info = malfunction.objects.get(id=data['id'])
        info.record_time = data['record_time']
        info.mal_details = data['mal_details']
        info.record_user = data['record_user']
        info.mal_reasons = data['mal_reasons']
        info.mal_status  = data['mal_status']
        info.recovery_time = data['recovery_time']
        info.time_all = data['time_all']
        info.handle_user = data['handle_user']
        info.save()
        return HttpResponse('更新成功！')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def MalfunctionDelete(request):
    clientip = request.META['REMOTE_ADDR']
    logger.info('user: %s' %request.user.username)
    username = request.user.username
    role = request.user.userprofile.role
    logger.info('%s %s is requesting. %s' %(clientip, username, request.get_full_path()))
    if role != u'cs':
        return HttpResponse('你没有删除的权限，请联系客服删除。')
    if request.method == 'POST':
        datas = json.loads(request.body)
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), datas))
        for data in datas:
            info = malfunction.objects.get(id=data['id'],)
            #return HttpResponse(info.record_time)
            info.delete()
        return HttpResponse('删除成功！')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')