from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
import json, logging
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from forms import UserForm
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('django')

@csrf_exempt 
def Login(request, template_name='login.html',):
    form = UserForm(request.POST)
    if form.is_valid():
        clientip = request.META['REMOTE_ADDR']
        username = form.username
        password = form.password
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponse('You have logined successfull!')
        
    return TemplateResponse(request, template_name)

@login_required
def index(request):
    return HttpResponse('welcome!')
