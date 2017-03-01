#!/usr//bin/env python
#-_- coding:utf-8 -_-
import os,sys,logging
import django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor.settings")
django.setup()
from check_tomcat.models import tomcat_project, tomcat_url, mail

#获取当前目录
current_dir = os.path.abspath(os.path.dirname(__file__))
#print basedir

cursor = django.db.connection.cursor()

tomcat_info_list = []
tomcat_project_list = []
mail_list = []
def get_list(filename, list_name):
    with open('%s/%s' %(current_dir,filename)) as f:
        lines = f.readlines()
    for line in lines:
        if line == '\n' or '#' in line:
            continue
        else:
            #print line.split('|')
            list_name.append(line.replace('\n', '').split('|'))

def update_tomcat_project():
    get_list('tomcat_project.txt', tomcat_project_list)
    info_list = tomcat_project.objects.all()
    for info in info_list:
        info.delete()
    cursor.execute('alter table check_tomcat_tomcat_project AUTO_INCREMENT=1; ')
    for tomcat_info in tomcat_project_list:
        if len(tomcat_info) != 7:
            continue
        else:
            info = tomcat_project(product=tomcat_info[0], project=tomcat_info[1], code_dir=tomcat_info[2], tomcat=tomcat_info[3], main_port=tomcat_info[4], script=tomcat_info[5], jdk=tomcat_info[6])
            info.save()

def update_tomcat_url():
    get_list('tomcat_info.txt', tomcat_info_list)
    info_list = tomcat_url.objects.all()
    for info in info_list:
        info.delete()
    cursor.execute('alter table check_tomcat_tomcat_url AUTO_INCREMENT=1; ')
    for url_info in tomcat_info_list:
        if len(url_info) != 3:
            continue
        else:
            info = tomcat_url(project=url_info[0], url=url_info[0],domain=url_info[2])
            info.save()

def update_mail():
    get_list('mail.txt', mail_list)
    info_list = mail.objects.all()
    for info in info_list:
        info.delete()
    cursor.execute('alter table check_tomcat_mail AUTO_INCREMENT=1; ')
    for mail_info in mail_list:
        if len(mail_info) != 4:
            continue
        else:
            info = mail(name=mail_info[0], mail_address=mail_info[1], status=mail_info[2], role=mail_info[3])
            info.save()
#
#def update_check_tomcat():
#    data = request.form 
#    result = db.check_tomcat(
#        time = data.get('time'),
#        project = data.get('project'),
#        domain = data.get('domain'),
#        url = data.get('url'),
#        code = data.get('code')
#    )
#    db.db.session.add(result)
#    db.db.session.commit()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        logging.error('No table specified.')
    elif sys.argv[1] == 'tomcat_url':
        logging.info('update table tomcat_url.')
        update_tomcat_url()
    elif sys.argv[1] == 'mail':
        logging.info('update table mail.')
        update_mail()
    elif sys.argv[1] == 'tomcat_project':
        logging.info('update table tomcat_project.')
        update_tomcat_project()
    else:
        logging.error('talbe %s doesn\'t exit.' %sys.argv[0])
