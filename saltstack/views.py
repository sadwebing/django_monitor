from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from monitor import settings
from saltstack.saltapi import SaltAPI
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

@csrf_protect
@login_required
def index(request):
    global clientip
    clientip = request.META['REMOTE_ADDR']
    title = u'saltstack'
    logger.info('%s is requesting.' %clientip)
    return render(
        request,
        'saltstack.html',
        {
            'clientip':clientip,
            'title': title,
        }
    )

