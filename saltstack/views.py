# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from monitor import settings
from check_tomcat.models import tomcat_project
from saltstack.saltapi import SaltAPI
from command import Command
import json, logging

logger = logging.getLogger('django')


# Create your views here.
@csrf_exempt
def CheckMinion(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        #print request.body
        #return HttpResponse("%s" %request.body)
        data     = json.loads(request.body)
        logger.info('%s is requesting %s. data: %s' %(clientip, request.get_full_path(), data))
        #logger.info('%s' %(data['tgt']))
        commandexe = Command(data['tgt'], 'test.ping')
        result   = commandexe.TestPing()
        return HttpResponse(result[data['tgt']])
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def GetProject(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        datas     = tomcat_project.objects.raw('select id,project from check_tomcat_tomcat_project where status="active";')
        projectlist = []
        for data in datas:
            projectlist.append(data.project)
        logger.info('%s is requesting. %s: %s' %(clientip, request.get_full_path(), projectlist))
        return HttpResponse(json.dumps(projectlist))
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def CommandExecute(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        data     = json.loads(request.body)
        logger.info('%s is requesting. %s 执行参数：%s' %(clientip, request.get_full_path(), data))
        commandexe = Command(data['target'], data['function'], data['arguments'], data['expr_form'])
        info = {}
        if data['function'] == 'test.ping':
            info = commandexe.TestPing()
        elif data['function'] == 'cmd.run':
            info = commandexe.CmdRun()
        elif data['function'] == 'state.sls':
            info = commandexe.StateSls()
        logger.info(json.dumps(info))
        return HttpResponse(json.dumps(info))
        #return HttpResponse(info)
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def CommandRestart(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        data     = json.loads(request.body)
        logger.info('%s is requesting. %s 执行参数：%s' %(clientip, request.get_full_path(), data))
        #results = []
        info = {}
        for project in data['project']:
            restart = tomcat_project.objects.filter(project=project).first().script
            if restart == '':
                arg = "/web/%s/bin/restart.sh" %project
            else:
                arg = "%s restart" %restart
            #logger.info(restart)
            arglist = ["runas=tomcat"]
            arglist.append(arg)
            logger.info("重启参数：%s"%arglist)
            commandexe = Command(data['target'], 'cmd.run', arglist, data['expr_form'])
            info[project] = commandexe.CmdRun()[data['target']]
            #logger.info(json.dumps(info))
        return HttpResponse(json.dumps(info))
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_protect
@login_required
def command(request):
    global username, role, clientip
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    global clientip
    clientip = request.META['REMOTE_ADDR']
    title = u'SALTSTACK-命令管理'
    logger.info('%s is requesting.' %clientip)
    return render(
        request,
        'saltstack/saltstack_index.html',
        {
            'clientip':clientip,
            'title': title,
            'role': role,
            'username': username,
        }
    )

@csrf_protect
@login_required
def restart(request):
    global clientip
    clientip = request.META['REMOTE_ADDR']
    title = u'SALTSTACK-服务重启'
    logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
    return render(
        request,
        'saltstack/saltstack_restart.html',
        {
            'clientip':clientip,
            'title': title,
            'role': role,
            'username': username,
        }
    )

@csrf_protect
@login_required
def Id(request):
    global clientip
    clientip = request.META['REMOTE_ADDR']
    title = u'SALTSTACK-ID管理'
    logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
    return render(
        request,
        'saltstack/saltstack_id.html',
        {
            'clientip':clientip,
            'title': title,
            'role': role,
            'username': username,
        }
    )

@csrf_exempt
def IdQuery(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        sapi = SaltAPI(
            url      = settings.SALT_API['url'],
            username = settings.SALT_API['user'],
            password = settings.SALT_API['password']
            )
        minionsup, minionsdown= sapi.MinionStatus()
        minion_list = []
        logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
        for minion_id in minionsup:
            minion_dict = {}
            minion_dict['minion_id'] = minion_id
            minion_dict['minion_status'] = 'up'
            minion_list.append(minion_dict)
        for minion_id in minionsdown:
            minion_dict = {}
            minion_dict['minion_id'] = minion_id
            minion_dict['minion_status'] = 'down'
            minion_list.append(minion_dict)
        return HttpResponse(json.dumps(minion_list))
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def QueryMinion(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        sapi = SaltAPI(
            url      = settings.SALT_API['url'],
            username = settings.SALT_API['user'],
            password = settings.SALT_API['password']
            )
        data = json.loads(request.body)
        logger.info('%s is requesting %s. minion: %s' %(clientip, request.get_full_path(), data))
        minion_id = data[0]['minion_id']
        info = sapi.GetGrains(minion_id)
        #logger.info(info['return'][0])
        return HttpResponse(json.dumps(info['return'][0]))
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')