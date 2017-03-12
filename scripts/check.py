#!/usr/bin/env python
#-_- coding:utf-8 -_-
import os,sys,datetime,logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
reload(sys)
sys.setdefaultencoding('utf8')
from scripts.tomcat import logger, send_mail, get_mail_list, check_tomcat, time, check_server_status, error_status
from scripts.salt import minionsdown

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

if __name__ == '__main__':
    if not check_server_status():
        os.system('nohup python %s/manage.py runserver 0.0.0.0:5000 &' %basedir)
        send_mail(get_mail_list('arno'), '%s Server Down!', "%s 不可用！" %(time(), server))
        logger.error('%s 不可用！' %server)
        sleep(3)
        if not check_server_status():
            send_mail(get_mail_list('arno'), '%s Server is unable to start, pls check!', "%s 服务起不来！" %(time(), server))
            logger.error('%s %s 服务起不来！' %(time(), server))
    content = check_tomcat()
    if content != "":
        send_mail(get_mail_list('arno', 'sa'),'tomcat报警',content,format='html')
    if len(minionsdown) != 0:
        send_mail(get_mail_list('arno', 'vincent'),'Attention','Minion Down:'+ '\n\t' +'\n\t'.join(minionsdown))
