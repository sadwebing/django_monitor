#!/usr/bin/env python
#-_- coding:utf-8 -_-
#author: Arno
#update: 2017/07/08  add multiprocessing
#        2017/07/11  add check_salt_intrm
#        2017/07/12  optimize check_server_status
#        2017/07/22  add color print

import os,sys,datetime,logging,multiprocessing,requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor.settings")
from check_tomcat.models import check_status
from scripts.tomcat import logger, send_mail, get_mail_list, check_tomcat, time, check_server_status, error_status, server
from time import sleep
from saltstack.saltapi import SaltAPI
from monitor import settings
from ctypes import c_char_p
from color_print import ColorP

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
admin_mail_addr = ['Arno@ag866.com']

salt_intrm = 'http://172.20.0.61:8080'
salt_intrm_id = 'EST_0_61'

sapi = SaltAPI(
    url      = settings.SALT_API['url'],
    username = settings.SALT_API['user'],
    password = settings.SALT_API['password']
)

def check_services_fun():
    check_services = check_status.objects.filter(program='check_services').first()
    if check_services.status == 1:
        content = check_tomcat()
        if content != "":
            send_mail(get_mail_list('check_services'),'tomcat报警',content,format='html')
    end_time['check_services'] = time()

def check_salt_minion_fun():
    check_salt_minion = check_status.objects.filter(program='check_salt_minion').first()
    if check_salt_minion.status == 1:
        minionsup, minionsdown= sapi.MinionStatus()
    else:
        minionsdown = []
    if len(minionsdown) != 0:
        send_mail(get_mail_list('check_salt_minion'),'Attention: salt_minion','Minion Down:'+ '\n\t' +'\n\t'.join(minionsdown))
    end_time['check_salt_minion'] = time()

def check_salt_intrm_false(salt_intrm_id, salt_intrm, status_code):
    result = sapi.checkMinion(
        tgt       = salt_intrm_id,
        expr_form = 'glob',
        )
    if result[0].has_key(salt_intrm_id):
        logger.info('%s status is %s.' %(salt_intrm_id, result[0][salt_intrm_id]))
        salt_intrm_id_status = result[0][salt_intrm_id]
    else:
        logger.error('%s status is down.' %salt_intrm_id)
        salt_intrm_id_status = 'not return'
    mail_content = (
        "-------------------------------------------------\n"
        "检测时间: %s\n"
        "检测服务: %s\n"
        "检测状态: %s\n"
        "%s: %s\n"
        "-------------------------------------------------"
        )%(time(), salt_intrm, status_code, salt_intrm_id, salt_intrm_id_status)
    send_mail(admin_mail_addr, 'Attention: salt_intrm check failed!', mail_content)

def check_salt_intrm():
    try:
        ret = requests.head(salt_intrm)
    except requests.exceptions.ConnectionError:
        logger.error('%s server is down or refused to connect.' %salt_intrm)
        check_salt_intrm_false(salt_intrm_id, salt_intrm, 'connection refused')
    except:
        logger.error('%s unkown error, pls check the script.' %salt_intrm)
        check_salt_intrm_false(salt_intrm_id, salt_intrm, 'unkown error, pls check the script')
    else:
        if ret.status_code == 200:
            logger.info('%s is running.' %salt_intrm)
        else:
            logger.error('%s check failed. Return status: %s' %(salt_intrm, ret.status_code))
            check_salt_intrm_false(salt_intrm_id, salt_intrm, ret.status_code)
    finally:
        end_time['check_salt_intrm'] = time()

if __name__ == '__main__':
    start_time = time()
    end_time = multiprocessing.Manager().dict()
    if not check_server_status():
        mail_content = (
            "-------------------------------------------------\n"
            "检测时间: %s\n"
            "检测服务: %s\n"
            "检测状态: %s\n"
            "-------------------------------------------------\n"
            )%(time(), server, '失败')
        os.system('nohup python %s/manage.py runserver 0.0.0.0:5000 &' %basedir)
        #send_mail(admin_mail_addr, 'Attention: django_server is down!', mail_content)
        mail_content = mail_content + (
            "尝试重启服务......\n"
            "重启时间: %s\n"
            )%time()
        sleep(4)
        if not check_server_status():
            mail_content = mail_content + (
                "检测状态: 失败\n"
                "-------------------------------------------------"
                )
            send_mail(admin_mail_addr, 'Attention: django_server is down!', mail_content)
            logger.error('%s %s 服务起不来！' %(time(), server))
        else:
            mail_content = mail_content + (
                "检测状态: 成功\n"
                "-------------------------------------------------"
                )
            send_mail(admin_mail_addr, 'Attention: django_server restarted!', mail_content)
            logger.error('%s %s 服务起不来！' %(time(), server))

    #multiprocessing two processes
    pw1 = multiprocessing.Process(target=check_services_fun, args=())
    pw2 = multiprocessing.Process(target=check_salt_minion_fun, args=())
    pw3 = multiprocessing.Process(target=check_salt_intrm, args=())
    pw1.start()
    pw2.start()
    pw3.start()
    pw1.join()
    pw2.join()
    pw3.join()
    print "start_time:                 " + ColorP("%s" %start_time,                    fore = 'green') 
    print "check_services_end_time:    " + ColorP("%s" %end_time['check_services'],    fore = 'yellow')  
    print "check_salt_minion_end_time: " + ColorP("%s" %end_time['check_salt_minion'], fore = 'yellow')  
    print "check_salt_intrm_time:      " + ColorP("%s" %end_time['check_salt_intrm'],  fore = 'yellow')  
    print "end_time:                   " + ColorP("%s" %time(),                        fore = 'green')