#-_- coding: utf-8 -_-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from dwebsocket import require_websocket, accept_websocket
import json, logging, requests, re
from accounts.limit import LimitAccess

logger = logging.getLogger('django')

@csrf_protect
@login_required
def index(request):
    title = u'检测中心'
    global username, role, clientip
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    clientip = request.META['REMOTE_ADDR']
    logger.info('%s is requesting %s' %(clientip, request.get_full_path()))
    return render(
        request,
        LimitAccess(role, 'detect/detect_index.html'),
        {
            #'title': title,
            'clientip':clientip,
            'role': role,
            'username': username,
        }
    )

@accept_websocket     
@csrf_exempt
def Execute(request):
    global username, role, clientip
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    clientip = request.META['REMOTE_ADDR']
    if request.is_websocket():
        for postdata in request.websocket:
            data = json.loads(postdata)
            logger.info('%s is requesting. %s 执行参数：%s' %(clientip, request.get_full_path(), data))

            req_ip = data['ip_network'] + '.' + str(data['ip_host_start']+data['step'])

            if data['port'] == '443':
            	url = 'https://' + req_ip + '/' +data['uri']
            else:
            	url = 'http://' + req_ip + ':' + data['port'] + '/' +data['uri']
            #logger.info(url)
            try:
            	ret = requests.get(url, verify=False, timeout=5)
            	#logger.info(ret.status_code)
            except requests.exceptions.ConnectionError:
            	data['http_code'] = 'Null'
            	data['title']     = ''
            else:
            	data['http_code'] = ret.status_code
            	try:
            	    title = re.search('<title>.*?</title>', ret.content)
            	    data['title'] = title.group().replace('<title>', '').replace('</title>', '')
            	except AttributeError:
            	    data['title'] = ''
            request.websocket.send(json.dumps(data))

        ### close websocket ###
        request.websocket.close()
