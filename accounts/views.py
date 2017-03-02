from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import tomcat_status
import json, logging
from django.contrib.auth.models import User


logger = logging.getLogger('django')

@csrf_exempt 
def login(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        data = json.loads(request.body)
        #status = "\t".join([data['access_time'], data['project'], data['domain'], data['url'], data['code'], data['info']])
        logger.info('%s is requesting. %s' %(clientip, data))
        status = tomcat_status(
            access_time = data['access_time'],
            project     = data['project'],
            domain      = data['domain'],
            url         = data['url'],
            code        = data['code'],
            info        = data['info'],
        )
        status.save()
        return HttpResponse("success!")
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')
