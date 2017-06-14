# coding: utf8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from dwebsocket import require_websocket
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from models import tomcat_status,tomcat_url, tomcat_project
from saltstack.command import Command
import json, logging, requests, re, datetime
logger = logging.getLogger('django')
error_status = 'null'

@csrf_exempt
def UrlQuery(request):
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
            datas = tomcat_url.objects.all()
        elif act == 'query_active':
            datas = tomcat_url.objects.filter(status='active')
        elif act == 'query_inactive':
            datas = tomcat_url.objects.filter(status='inactive')
        else:
            return HttpResponse("参数错误！")
        logger.info('查询参数：%s' %act)
        url_list = []
        for url in datas:
            tmp_dict = {}
            tmp_dict['id'] = url.id
            tmp_dict['project'] = url.project
            tmp_dict['server_ip'] = url.server_ip
            tmp_dict['server_type'] = url.server_type
            tmp_dict['role'] = url.role
            tmp_dict['domain'] = url.domain
            tmp_dict['url'] = url.url
            tmp_dict['status_'] = url.status
            tmp_dict['info'] = url.info
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
            info = tomcat_url.objects.get(project=data['project'], server_ip=data['server_ip'])
            logger.info('%s is requesting. %s url: %s  already exists!' %(clientip, request.get_full_path(), info.url))
            return HttpResponse('记录: %s %s already exists!' %(info.project, info.server_ip))
        except:
            logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))
            info = tomcat_url(project=data['project'], server_ip=data['server_ip'].strip(),server_type=data['server_type'] , role=data['role'], domain=data['domain'], url=data['url'], status=data['status_'], info=data['info'])
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
        info.server_ip = data['server_ip'].strip()
        info.server_type = data['server_type']
        info.role = data['role']
        info.domain  = data['domain']
        info.url     = data['url']
        info.status = data['status_']
        info.info = data['info']
        info.save()
        return HttpResponse('更新成功！')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt 
def UrlUpdateStatus(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        data = json.loads(request.body)
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))
        info = tomcat_url.objects.get(id=data['id'])
        info.status = data['status']
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

@require_websocket
@csrf_exempt
def UrlCheckServer(request):
    if request.is_websocket():
        global username, role, clientip
        username = request.user.username
        try:
            role = request.user.userprofile.role
        except:
            role = 'none'
        clientip = request.META['REMOTE_ADDR']
        #logger.info(dir(request.websocket))
        #message = request.websocket.wait()
        for postdata in request.websocket:
            #logger.info(type(postdata))
            data = json.loads(postdata)
            ### step one ###
            info_one = {}
            info_one['step'] = 'one'
            request.websocket.send(json.dumps(info_one))
            logger.info('%s is requesting. %s 执行参数：%s' %(clientip, request.get_full_path(), data))
            #results = []
            ### final step ###
            info_final = {}
            info_final['step'] = 'final'

            info_final['access_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            commandexe = Command(data['server_ip'], 'test.ping')
            test_result = commandexe.TestPing()[data['server_ip']]
            if test_result == 'not return':
                info_final['code'] = 'null'
                info_final['info'] = '请检查服务器是否存活'
            else:
                try:
                    if data['server_type'] == 'app':
                        info_final['info'] = error_status
                        datas = {}
                        datas['target'] = data['server_ip']
                        datas['function'] = 'cmd.run'
                        datas['arguments'] = 'ps -ef |grep -i "java" |grep -i " -jar" |grep -v grep'
                        datas['expr_form'] = 'glob'
                        commandexe = Command(datas['target'], datas['function'], datas['arguments'], datas['expr_form'])
                        exe_result = commandexe.CmdRun()[datas['target']]
                        #logger.info("exe_result: %s" %exe_result)
                        if exe_result == '':
                            info_final['code'] = 'null'
                        else:
                            info_final['code'] = '200'
                        #logger.info(info_final)
                    else:
                        ret = requests.head(data['url'], headers={'Host': data['domain']}, timeout=10)
                        info_final['code'] = '%s' %ret.status_code
                        try:
                            title = re.search('<title>.*?</title>', ret.content)
                            info_final['info'] = title.group().replace('<title>', '').replace('</title>', '')
                        except AttributeError:
                            info_final['info'] = error_status
                except:
                    info_final['code'] = error_status
                    info_final['info'] = error_status

            request.websocket.send(json.dumps(info_final))
        ### close websocket ###
        request.websocket.close()