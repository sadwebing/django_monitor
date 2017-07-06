#!/usr/bin/env python
#-_- coding:utf-8 -_-
import os,sys,datetime,logging,multiprocessing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor.settings")
from check_tomcat.models import check_status
from scripts.tomcat import logger, send_mail, get_mail_list, check_tomcat, time, check_server_status, error_status, server
from time import sleep
from saltstack.saltapi import SaltAPI
from monitor import settings

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def check_services_fun():
    check_services = check_status.objects.filter(program='check_services').first()
    if check_services.status == 1:
        content = check_tomcat()
        if content != "":
            send_mail(get_mail_list('check_services'),'tomcat报警',content,format='html')

def check_salt_minion_fun():
    check_salt_minion = check_status.objects.filter(program='check_salt_minion').first()
    #if check_salt_minion.status == 1:
    #    from scripts.salt import minionsdown
    #else:
    #    minionsdown = []
    if check_salt_minion.status == 1:
        sapi = SaltAPI(
            url      = settings.SALT_API['url'],
            username = settings.SALT_API['user'],
            password = settings.SALT_API['password']
        )
        minionsup, minionsdown= sapi.MinionStatus()
    else:
        minionsdown = []
    if len(minionsdown) != 0:
        send_mail(get_mail_list('check_salt_minion'),'Attention','Minion Down:'+ '\n\t' +'\n\t'.join(minionsdown))


if __name__ == '__main__':
    start_time_2 = time()
    #print start_time_2
    if not check_server_status():
        os.system('nohup python %s/manage.py runserver 0.0.0.0:5000 &' %basedir)
        send_mail(['Arno@ag866.com'], '%s Server Down!' %server, "%s %s 不可用！" %(time(), server))
        logger.error('%s 不可用！' %server)
        sleep(3)
        if not check_server_status():
            send_mail(['Arno@ag866.com'], '%s Server is unable to start, pls check!' %server, "%s %s 服务起不来！" %(time(), server))
            logger.error('%s %s 服务起不来！' %(time(), server))
    pool = multiprocessing.Pool(processes=5)
    pool.apply_async(check_salt_minion_fun())
    pool.apply_async(check_services_fun())
    pool.close()
    pool.join()
    #check_salt_minion_fun()
    #check_services_fun()
    print "start2 at: " + start_time_2
    print "end2   at: " + time()
