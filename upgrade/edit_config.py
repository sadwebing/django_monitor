# coding: utf-8
from models import op_history
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
import logging, datetime, requests, svn.remote, os, shutil, json, platform
from monitor import settings
from scripts.tomcat import time

logger = logging.getLogger('django')

class svn_config(object):
    def __init__(self, data):
        self.__data = data
        self.__results = {}
        self.__results['files'] = {}
        self.__conf_url = os.path.abspath(os.path.dirname(__file__)) + '/conf'
        try:
            self.__data['envir']
        except Exception as e:
            logger.error('传入参数envir，不存在，请检查: %s' %self.__data)
            self.__results['code'] = 500
            self.__results['response'] = '传入参数envir，不存在，请检查！'
            return self.__results
        else:
            if data['envir'] == 'ONLINE':
                self.__svn_url = settings.SVN_URL.rstrip('/') + '/sa/ONLINE_CONF/' + self.__data['project']
                self.__conf_url = self.__conf_url + '/online/' + self.__data['project']
            elif data['envir'] == 'UAT':
                self.__svn_url = settings.SVN_URL.rstrip('/') + '/sa/UAT_CONF/UAT_' + self.__data['project']
                self.__conf_url = self.__conf_url + '/uat/' + self.__data['project']
            else:
                logger.error('传入参数envir: %s 不正确，请检查！' %self.__data['envir'])
                self.__results['code'] = 500
                self.__results['response'] = '传入参数envir: %s 不正确，请检查！' %self.__data['envir']
                return self.__results

        if 'Windows' in platform.system():
            self.__conf_url = self.__conf_url.replace('/', '\\')
            self.__sep = '\\'
        else:
            self.__sep = '/'

        self.__ret = svn.remote.RemoteClient(self.__svn_url, username=settings.SVN_USERNAME, password=settings.SVN_PASSWORD)

    def getFiles(self):
        try:
            #if os.path.exists(self.__conf_url):
            #    shutil.rmtree(self.__conf_url)
            #self.__ret.checkout(self.__conf_url)
            self.__ret.export(self.__conf_url, force=True)
        except Exception as e:
            logger.error(e)
            self.__results['code'] = 500
            self.__results['response'] = '获取SVN配置文件失败，请检查日志！'
        else:
            logger.info('获取配置文件成功：%s' %self.__data)
            self.__results['code'] = 200
            self.__results['response'] = '获取配置文件成功！'
            file_list = os.listdir(self.__conf_url)
            for file in file_list:
                if os.path.isfile(self.__conf_url+self.__sep+file):
                    with open(self.__conf_url+self.__sep+file, 'r') as re:
                        self.__results['files'][file] = re.readlines()
        return self.__results

    def commitFiles(self):
        if os.path.exists(self.__conf_url):
            pass
        else:
            os.mkdir(self.__conf_url)
        self.__ret.checkout(self.__conf_url)
        try:
            for file in os.listdir(self.__conf_url):
                if os.path.isfile(self.__conf_url+self.__sep+file):
                    os.remove(self.__conf_url+self.__sep+file)
            for file, content in self.__data['files'].iteritems():
                with open(self.__conf_url+self.__sep+file, 'w') as re:
                    re.writelines(content)
            commit_log = self.__ret.run_command('commit', ['-m "%s"' %self.__data['commit'], self.__conf_url])
            logger.info(commit_log)
        except Exception as e:
            logger.error(e)
            self.__results['code'] = 500
            self.__results['response'] = 'SVN commit 配置文件失败，请检查日志！'
            logger.info('文件可能存在冲突，将当前修改文件设定为最新状态，再提交一次commit。')
            try:
                for file in self.__data['files']:
                    commit_log = self.__ret.run_command('resolve', ['--accept=working', self.__conf_url+self.__sep+file])
                    logger.info(commit_log)
                commit_log = self.__ret.run_command('commit', ['-m "%s"' %self.__data['commit'], self.__conf_url])
                logger.info(commit_log)
            except:
                logger.error(e)
            else:
                logger.info('SVN commit 配置文件成功：%s' %self.__data['commit'])
                self.__results['code'] = 200
                self.__results['response'] = 'SVN commit 配置文件成功！'

        else:
            logger.info('SVN commit 配置文件成功：%s' %self.__data['commit'])
            self.__results['code'] = 200
            self.__results['response'] = 'SVN commit 配置文件成功！'
        return self.__results

@csrf_exempt
@login_required
def EditConfig(request):
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    clientip = request.META['REMOTE_ADDR']
    if role != 'sa':
        return HttpResponseForbidden('你没有权限进行编辑。')
    data = json.loads(request.body)
    logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
    if data['act'] == 'getfiles':
        ret = svn_config(data).getFiles()
        if ret['code'] == 200:
            return HttpResponse(json.dumps(ret))
        elif ret['code'] == 500:
            return HttpResponseServerError(ret['response'])
    elif data['act'] == 'commitfiles':
        data['commit'] = "%s %s %s commit svn config files: %s %s %s"%(time(), clientip, username, data['envir'], data['project'], data['svn_id'])
        ret = svn_config(data).commitFiles()
        if ret['code'] == 200:
            return HttpResponse(ret['response'])
        elif ret['code'] == 500:
            return HttpResponseServerError(ret['response'])