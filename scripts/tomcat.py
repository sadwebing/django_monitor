#!/usr/bin/env python
#-_- coding:utf-8 -_-
import re,os,sys,smtplib,requests,datetime,logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from time import sleep
from email.mime.text import MIMEText
from email.header import Header
reload(sys)
sys.setdefaultencoding('utf8')
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor.settings")
django.setup()
from check_tomcat.models import tomcat_url, mail, tomcat_status, server_status


basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
server = 'http://192.168.100.107:5000/monitor_server'
requests.adapters.DEFAULT_RETRIES = 3

def send_mail(to_list,sub,content):
    sender = 'monitor@ag866.com'
    msg = MIMEText(str(content),'html','utf-8')#中文需参数‘utf-8’，单字节字符不需要  
    msg['Subject'] = Header(sub, 'utf-8')
    msg['From'] = sender
    msg['To'] = ';'.join(to_list)
    try:
        smtp = smtplib.SMTP()
        smtp.connect('localhost')
        smtp.sendmail(sender, to_list, msg.as_string())
        logging.info('[success]mail from %s, mail to %s, %s' %(sender, to_list, content))
        smtp.quit()
        return True
    except Exception, e:
        logging.error('[failed]mail from %s, mail to %s, %s' %(sender, to_list, content))
        return False

def get_mail_list(list_name):
    url_all = mail.objects.all()
    for mail_info in url_all:
        if mail_info.status == 'active':
            list_name.append(mail_info.mail_address)
    logging.info('get mail_list successful.')
    #return mail_list
def check_tomcat(context_body):
    url_all = tomcat_url.objects.all()
    for tomcat_info in url_all:
        result = {}
        result['time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        result['project'] = tomcat_info.project
        result['domain'] = tomcat_info.domain
        result['url'] = tomcat_info.url
        try:
            ret = requests.get(result['url'], headers={'Host': result['domain']}, timeout=connect_timeout)
            result['code'] = ret.status_code
            try:
                title = re.search('<title>.*?</title>', ret.content)
                result['info'] = title.group().replace('<title>', '').replace('</title>', '')
            except AttributeError:
                result['info'] = error_status
        except requests.exceptions.ConnectionError:
            result['code'] = error_status
            result['info'] = error_status
        print result['code']
        status = server_status.objects.order_by('-id').first()
        if status.status == '200':
            try:
                ret2 = requests.post(server, data=result, timeout=3)
            except requests.exceptions.ConnectionError:
                record = server_status(access_time=current_time, url=server, status=error_status, info='null')
                record.save()
                send_mail(mail_list, 'Server Down!', "%s 不可用！" %server)
                logging.error('%s 不可用！' %server)
        if result['code'] not in code_list:
            print result['code']
            context_body = context_body + "<tr style=\"font-size:15px\"><td >%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" %(result['time'], result['project'], result['domain'], result['url'], result['code'], result['info'])
        #logging.info(MIMEText(str(result), 'utf-8'))
    return context_body

def time():
    current_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    return current_time

def check_server_status():
    try:
        ret = requests.get(server,timeout=2)
        record = server_status(access_time=time(), url=server, status=ret.status_code, info=ret.text)
        record.save()
        return True
    except requests.exceptions.ConnectionError:
        record = server_status(access_time=time(), url=server, status=error_status, info='null')
        record.save()
        return False

if __name__ == '__main__':
    current_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    error_status = 'null'
    connect_timeout=10
    mail_list = []
    get_mail_list(mail_list)
    if not check_server_status():
        os.system('nohup python %s/manage.py runserver 0.0.0.0:5000 &' %basedir)
        send_mail(mail_list, 'Server Down!', "%s 不可用！" %server)
        logging.error('%s 不可用！' %server)
        sleep(3)
        if not check_server_status():
            send_mail(mail_list, 'Server is unable to start, pls check!', "%s 服务起不来！" %server)
            logging.error('%s 服务起不来！' %server)
    #code_list = [200, 302]
    code_list = [200, 302, 405]
    content_head = """\
    <html><head><title>HTML email</title></head><body>
    <table  borderColor=red cellPadding=1 width=1000 border=1 cellspacing=\"1\" style=\"text-align:center;padding:1px\">
    <tr style=\"font-size:14px\">
    <th style="width:120px">时间</th> 
    <th style="width:120px">工程</th> 
    <th style="width:120px">域名</th> 
    <th style="width:300px">路径</th> 
    <th style="width:60px">状态</th> 
    <th style="width:120px">备注</th>
    </tr>
    """
    content_body=""
    content_body = check_tomcat(content_body)
    if content_body != "":
        content = content_head + content_body + "</table></body></html>"
        send_mail(mail_list,'tomcat报警',content)
