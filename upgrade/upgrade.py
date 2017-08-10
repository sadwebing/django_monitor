# coding: utf-8
from models import op_history
import logging, datetime, requests
from monitor import settings

logger = logging.getLogger('django')

class Upgrade(object):
    def __init__(self, data, username, clientip):
        if isinstance(data, dict):
            self.__data             = data
            self.__data['username'] = username
            self.__data['clientip'] = clientip
            self.__data['api']      = settings.UPGRADE_API
            self.__data['timeout']  = 1200
            #try:
            #    if self.__data['step'] == 0:
            #        self.__data['act'] = 'getfile'
            #except KeyError, e:
            #    logger.error('%s %s upgrade args KeyError: %s' %(self.__data['clientip'], self.__data['username'], self.__data))
            #    return None
            #except:
            #    logger.error('%s %s upgrade args UnknownError: %s' %(self.__data['clientip'], self.__data['username'], self.__data))
            #    return None
        else:
            logger.error('%s %s upgrade args error: %s' %(clientip, username, data))
            return None

    def getHosts(self):
        self.__data['exe_api'] = self.__data['api'] + '?project=%s&action=gethost' %(self.__data['project'][0])
        self.__data['timeout'] = 60
        try:
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
        #if self.__data['act'] == 'getfile':
        #    self.__data['exe_api'] = self.__data['api'] + '?project=%s&act=%s&svn_id=%s' %(self.__data['project'], self.__data['act'], self.__data['svn_id'])
        #else:
        #    self.__data['exe_api'] = self.__data['api'] + '?project=%s&ip_addr=%s&act=%s&restart=%s' %(self.__data['project'], self.__data['ip_addr'][self.__data['step']-1], self.__data['act'], self.__data['restart'])
        self.__data['exe_api'] = self.__data['api'] + '?project=%s&ip_addr=%s&action=%s&restart=%s&svn_id=%s&envir=%s' %(self.__data['project'], self.__data['ip_addr'][self.__data['step']-1], self.__data['act'], self.__data['restart'], self.__data['svn_id'], self.__data['envir'])
        try:
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
            logger.info("%s, %s success!" %(self.__data['exe_api'], self.__data['act']))
            self.__data['result'] = ret.content
            self.__data['op_status'] = 1
        finally:
            try:
                op_record = op_history(
                    svn_id     = self.__data['svn_id'],
                    project    = self.__data['project'],
                    ip_addr    = self.__data['ip_addr'][self.__data['step']-1],
                    act        = self.__data['act'],
                    op_user    = self.__data['username'],
                    op_ip_addr = self.__data['clientip'],
                    op_status  = self.__data['op_status'],
                    envir      = self.__data['envir'],
                    info       = self.__data['result'],
                    op_time    = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                    )
                #op_record.save()
            except:
                self.__data['result'] = 'InsertRecordError'
                self.__data['op_status'] = 0
                logger.error('insert into upgrade_op_history failed: %s' %self.__data)
            finally:
                return self.__data