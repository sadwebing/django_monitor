# coding: utf-8
from models import op_history
import logging, datetime, requests, json
from monitor import settings
from scripts.tomcat import time
from time import sleep

logger = logging.getLogger('django')

class Upgrade(object):
    def __init__(self, data, username, clientip):
        #数据初始化，针对回退与升级，比对代码不同的数据构造
        if isinstance(data, dict):
            if data['act'] == 'gethosts':
                self.__data = data
            elif data['act'] == 'rollback':
                self.__data             = data['dict']
                self.__data['step']     = data['step']
                self.__data['act']      = data['act']
                self.__data['restart']  = data['restart']
            else:
                self.__data            = data
                self.__data['ip_addr'] = self.__data['ip_addr'][self.__data['step']-1]
            self.__data['username'] = username
            self.__data['clientip'] = clientip
            self.__data['api']      = settings.UPGRADE_API  #api获取
            self.__data['timeout']  = 1200  #默认超时时间
        else:
            logger.error('%s %s upgrade args error: %s' %(clientip, username, data))
            return None

    def getHosts(self):
        #获取工程主机列表
        self.__data['exe_api'] = self.__data['api'] + '?project=%s&action=gethost' %(self.__data['project'][0])  #执行api
        self.__data['timeout'] = 60  #获取列表超时时间设置
        try:
            #执行get请求
            ret = requests.get(self.__data['exe_api'], timeout=self.__data['timeout'])
        except requests.exceptions.ReadTimeout:
            logger.error("%s, ReadTimeout! timeout: %s s" %(self.__data['exe_api'], self.__data['timeout']))
            self.__data['result'] = '%s ReadTimeout' %self.__data['exe_api']
            self.__data['op_status'] = 0
        except requests.exceptions.ConnectionError:
            logger.error("%s, ConnectionError!" %self.__data['exe_api'])
            self.__data['result'] = '%s ConnectionError' %self.__data['exe_api']
            self.__data['op_status'] = 0
        except:
            logger.error("%s, UnknownError!" %(self.__data['exe_api']))
            self.__data['result'] = '%s UnknownError' %self.__data['exe_api']
            self.__data['op_status'] = 0
        else:
            logger.info("%s, request success!" %self.__data['exe_api'])
            self.__data['result'] = ret.content
            self.__data['op_status'] = 1
        finally:
            return self.__data

    def Execute(self):
        #执行升级，比对代码和回退
        if self.__data['act'] == 'rollback':
            #执行回退的api
            self.__data['exe_api'] = self.__data['api'] + '?project=%s&ip_addr=%s&action=%s&restart=%s&backup_file=%s&envir=%s' %(self.__data['project'], self.__data['ip_addr'], self.__data['act'], self.__data['restart'], self.__data['backup_file'], self.__data['envir'])
        else:
            #执行升级和比对代码的api
            self.__data['exe_api'] = self.__data['api'] + '?project=%s&ip_addr=%s&action=%s&restart=%s&svn_id=%s&envir=%s' %(self.__data['project'], self.__data['ip_addr'], self.__data['act'], self.__data['restart'], self.__data['svn_id'], self.__data['envir'])
        try:
            self.__data['op_time'] = time()
            #执行get请求
            ret = requests.get(self.__data['exe_api'], timeout=self.__data['timeout'])
        except requests.exceptions.ReadTimeout:
            logger.error("%s, ReadTimeout! timeout: %s s" %(self.__data['exe_api'], self.__data['timeout']))
            self.__data['result'] = '%s ReadTimeout' %self.__data['exe_api']
            self.__data['op_status'] = 0
            self.__data['com_time'] = time()
        except requests.exceptions.ConnectionError:
            logger.error("%s, ConnectionError!" %self.__data['exe_api'])
            self.__data['result'] = '%s ConnectionError' %self.__data['exe_api']
            self.__data['op_status'] = 0
            self.__data['com_time'] = time()
        except:
            logger.error("%s, UnknownError!" %(self.__data['exe_api']))
            self.__data['result'] = '%s UnknownError' %self.__data['exe_api']
            self.__data['op_status'] = 0
            self.__data['com_time'] = time()
        else:
            logger.info("%s, %s success!" %(self.__data['exe_api'], self.__data['act']))
            self.__data['result'] = ret.content
            self.__data['op_status'] = 1
            self.__data['com_time'] = time()
        finally:
            try:
                self.__data['result'] = json.loads(self.__data['result'])
                self.__data['info']   = self.__data['result'][self.__data['act']]
            except ValueError:
                logger.error('%s result is string: %s' %(self.__data['act'], self.__data['result']))
                self.__data['info']   = self.__data['result']
            except:
                logger.error('%s result doesn\'t has key %s: %s' %(self.__data['act'], self.__data['act'], self.__data['result']))
                self.__data['info']   = self.__data['result']

            if self.__data['act'] == 'deploy':
                try:
                    self.__data['backup_file'] = self.__data['result']['backup_file']
                except:
                    logger.error('deploy result doesn\'t has key backup_file: %s' %self.__data['result'])
                    self.__data['backup_file'] = 'Null'
            elif self.__data['act'] == 'diff':
                self.__data['backup_file'] = 'Null'

            try:
                op_record = op_history(
                    svn_id      = self.__data['svn_id'],
                    project     = self.__data['project'],
                    ip_addr     = self.__data['ip_addr'],
                    act         = self.__data['act'],
                    op_user     = self.__data['username'],
                    op_ip_addr  = self.__data['clientip'],
                    op_status   = self.__data['op_status'],
                    envir       = self.__data['envir'],
                    info        = self.__data['info'],
                    op_time     = self.__data['op_time'],
                    com_time    = self.__data['com_time'],
                    backup_file = self.__data['backup_file'],
                    )
                op_record.save()
            except:
                self.__data['result'] = 'InsertRecordError'
                self.__data['op_status'] = 0
                logger.error('insert into upgrade_op_history failed: %s' %self.__data)
            finally:
                return self.__data