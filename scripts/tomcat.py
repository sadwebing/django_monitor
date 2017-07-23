#!/usr/bin/env python
#-_- coding:utf-8 -_-
#author: Arno
#update: 2017/07/07 add multiprocessing pool
#        2017/07/11 optimize send_mail
#        2017/07/13 update check app server
#        2017/07/22 add color print

import re,os,sys,smtplib,requests,datetime,logging,multiprocessing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from time import sleep
from saltstack.command import Command
from email.mime.text import MIMEText
from email.header import Header
reload(sys)
sys.setdefaultencoding('utf8')
import django,json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor.settings")
django.setup()
from check_tomcat.models import tomcat_url, mail, tomcat_status, server_status, tomcat_project
from color_print import ColorP

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
server = 'http://192.168.100.107:5000/monitor_server/check/'
requests.adapters.DEFAULT_RETRIES = 3
logger = logging.getLogger('django')
error_status = 'null'

def send_mail(to_list,sub,content,format=''):
    sender = 'monitor@ag866.com'
    msg = MIMEText(str(content),format,'utf-8')#中文需参数‘utf-8’，单字节字符不需要  
    msg['Subject'] = Header(sub, 'utf-8')
    msg['From'] = sender
    msg['To'] = ';'.join(to_list)
    try:
        smtp = smtplib.SMTP()
        smtp.connect('localhost')
        smtp.sendmail(sender, to_list, msg.as_string())
        logger.info('[success]mail from %s, mail to %s \n%s' %(sender, to_list, content))
        smtp.quit()
        return True
    except Exception, e:
        logger.error('[failed]mail from %s, mail to %s \n%s' %(sender, to_list, content))
        return False

def get_mail_list(program):
    mail_list = []
    datas = mail.objects.raw('select * from check_tomcat_mail where %s=1;' %program)
    for data in datas:
        mail_list.append(data.mail_address)
    return mail_list

def get_result(result, tomcat_info, code_list, content_body):
    try:
        if tomcat_info.server_type == 'app':
            result['info'] = error_status
            datas = {}
            datas['target'] = tomcat_info.minion_id
            datas['function'] = 'cmd.run'
            datas['arguments'] = 'ps -ef |grep -i "java" |grep -i " -jar" |grep -v grep'
            datas['expr_form'] = 'glob'
            commandexe = Command(datas['target'], datas['function'], datas['arguments'], datas['expr_form'])
            exe_result = commandexe.CmdRun()[datas['target']]
            if exe_result == '':
                result['code'] = error_status
            elif exe_result == 'not return':
                result['code'] = exe_result
                result['info'] = '请检查服务器是否存活'
            else:
                result['code'] = '200'
                result['info'] = '正常'
            #logger.info(result)
        else:
            ret = requests.head(result['url'], headers={'Host': result['domain']}, timeout=16)
            if tomcat_info.project =='ALL_TSD_WS' and ret.status_code == 500:
                result['code'] = '200'
            else:
                result['code'] = '%s' %ret.status_code
            try:
                title = re.search('<title>.*?</title>', ret.content)
                result['info'] = title.group().replace('<title>', '').replace('</title>', '')
            except AttributeError:
                if result['code'] in code_list:
                    result['info'] = '正常'
                else:
                    result['info'] = '失败'
    except:
        result['code'] = error_status
        result['info'] = '失败'
    if result['code'] == error_status:
        commandexe = Command(tomcat_info.minion_id, 'test.ping')
        test_result = commandexe.TestPing()[tomcat_info.minion_id]
        if test_result == 'not return':
            result['code'] == test_result
            result['info'] = '请检查服务器是否存活'
    #print "  %s" %result['code']
    try:
        ret = requests.post(server, data=json.dumps(result), timeout=3)
    except requests.exceptions.ConnectionError:
        insert = tomcat_status(
            access_time = result['access_time'],
            project     = result['project'],
            domain      = result['domain'],
            url         = result['url'],
            code        = result['code'],
            info        = result['info'],
        )
        insert.save()
    if result['code'] not in code_list:
        print ColorP(result['code'], fore = 'red') + "    " + result['project'] + ":  " +  result['url']
        try:
            result['server_type'] = tomcat_project.objects.filter(project=result['project']).first().server_type
        except:
            send_mail(['Arno@ag866.com'],'tomcat报警','%s project doesn\'t exists' %result['project'])
            result['server_type'] = 'unknown'
        content_body = content_body + "<tr style=\"font-size:15px\"><td >%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" %(result['access_time'], result['project'], result['server_type'], result['domain'], result['url'], result['code'], result['info'])
    else:
        print result['code'] + "    " + result['project'] + ":  " +  result['url']

    #logger.info(MIMEText(str(result), 'utf-8'))
    return content_body

def check_tomcat():
    content_head = """\
    <html><head><title>HTML email</title></head><body>
    <table  borderColor=red cellPadding=1 width=1000 border=1 cellspacing=\"1\" style=\"text-align:center;padding:1px\">
    <tr style=\"font-size:14px\">
    <th style="width:120px">时间</th> 
    <th style="width:120px">工程</th> 
    <th style="width:120px">服务类型</th> 
    <th style="width:120px">域名</th> 
    <th style="width:300px">路径</th> 
    <th style="width:120px">状态</th> 
    <th style="width:300px">备注</th>
    </tr>
    """
    content_body = ""
    content = ""
    pool = multiprocessing.Pool(processes=25)
    url_all = tomcat_url.objects.filter(status='active').all()
    code_list = ['200', '302', '303', '405']
    for tomcat_info in url_all:
        global result
        result = {}
        result['access_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        result['project'] = tomcat_info.project
        result['domain'] = tomcat_info.domain
        result['url'] = tomcat_info.url

        content_body = pool.apply_async(get_result, (result, tomcat_info, code_list, content_body, )).get()
        #result['code'], result['info'] = get_result(result, tomcat_info, code_list)
        
        if content_body != "":
            content = content_head + content_body + "</table></body></html>"
    pool.close()
    pool.join()
    return content

def time():
    current_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    return current_time

def check_server_status():
    try:
        ret = requests.get(server,timeout=2)
        record = server_status(access_time=time(), url=server, status=ret.status_code, info=ret.text)
        record.save()
        logger.info('%s is running.' %server)
        return True
    except requests.exceptions.ConnectionError:
        record = server_status(access_time=time(), url=server, status=error_status, info='null')
        record.save()
        logger.error('%s check failed.' %server)
        return False

if __name__ == '__main__':
    print "使用check.py"