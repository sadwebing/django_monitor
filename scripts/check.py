#!/usr/bin/env python
#-_- coding:utf-8 -_-
import os,sys,datetime,logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor.settings")
from check_tomcat.models import check_status
from scripts.tomcat import logger, send_mail, get_mail_list, check_tomcat, time, check_server_status, error_status

check_salt_minion = check_status.objects.filter(program='check_salt_minion').first()
if check_salt_minion.status == 1:
    from scripts.salt import minionsdown
else:
    minionsdown = []

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

if __name__ == '__main__':
    if not check_server_status():
        os.system('nohup python %s/manage.py runserver 0.0.0.0:5000 &' %basedir)
        send_mail(['Arno@ag866.com'], '%s Server Down!' %server, "%s %s 不可用！" %(time(), server))
        logger.error('%s 不可用！' %server)
        sleep(3)
        if not check_server_status():
            send_mail(['Arno@ag866.com'], '%s Server is unable to start, pls check!' %server, "%s %s 服务起不来！" %(time(), server))
            logger.error('%s %s 服务起不来！' %(time(), server))
    check_services = check_status.objects.filter(program='check_services').first()
    if check_services.status == 1:
        content = check_tomcat()
        if content != "":
            send_mail(get_mail_list('check_services'),'tomcat报警',content,format='html')
    if len(minionsdown) != 0:
        send_mail(get_mail_list('check_salt_minion'),'Attention','Minion Down:'+ '\n\t' +'\n\t'.join(minionsdown))
