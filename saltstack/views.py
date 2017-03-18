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
#get saltapi url
sapi = SaltAPI(
    url      = settings.SALT_API['url'],
    username = settings.SALT_API['user'],
    password = settings.SALT_API['password']
    )

# Create your views here.
@csrf_exempt
def CheckMinion(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        #print request.body
        #return HttpResponse("%s" %request.body)
        data     = json.loads(request.body)
        logger.info('%s is requesting. %s' %(clientip, data))
        #logger.info('%s' %(data['tgt']))
        result   = sapi.checkMinion(data['tgt'])
        if len(result['return'][0]) != 0:
            return HttpResponse("True")
        else:
            return HttpResponse("False")
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
        logger.info(info)
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
        results = []
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
            result = sapi.ClientLocal(
                tgt       = data['target'],
                fun       = 'cmd.run',
                arg       = arglist,
                expr_form = data['expr_form'],
                )
            info[project] = result['return'][0][data['target']]
            logger.info(info)
        return HttpResponse(json.dumps(info))
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_protect
@login_required
def command(request):
    global clientip
    clientip = request.META['REMOTE_ADDR']
    title = u'SALTSTACK-命令管理'
    logger.info('%s is requesting.' %clientip)
    return render(
        request,
        'saltstack_index.html',
        {
            'clientip':clientip,
            'title': title,
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
        'saltstack_restart.html',
        {
            'clientip':clientip,
            'title': title,
        }
    )

@csrf_protect
@login_required
def id(request):
    global clientip
    clientip = request.META['REMOTE_ADDR']
    title = u'SALTSTACK-ID管理'
    logger.info('%s is requesting.' %clientip)
    return render(
        request,
        'saltstack_id.html',
        {
            'clientip':clientip,
            'title': title,
        }
    )

