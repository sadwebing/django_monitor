# -*- coding: utf-8 -*-

import requests,json
from monitor import settings
import json, logging
logger = logging.getLogger('django')

class SaltAPI(object):
    def __init__(self, url, username, password):
        self.__url = url.rstrip('/')
        self.__user = username
        self.__password = password
        self.__token_id = self.saltLogin()

    def saltLogin(self):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        url = self.__url + '/login'
        ret = requests.post(url, data=params, verify=False)
        token = ret.headers['X-Auth-Token']
        return token

    def checkMinion(self, tgt, expr_form='list'):
        if tgt == '*':
            params = {'client': 'local', 'tgt': tgt, 'fun': 'test.ping'}
        else:
            params = {'client': 'local', 'tgt': tgt, 'fun': 'test.ping', 'expr_form': expr_form}
        ret = requests.post(url=self.__url, data=params, headers={'X-Auth-Token': self.__token_id}, verify=False)
        return ret.json()['return']

    def ClientLocal(self, tgt, fun, arg, expr_form='list', timeout=300):
        if tgt == '*':
            params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        else:
            params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        try:
            ret = requests.post(url=self.__url, data=params, headers={'X-Auth-Token': self.__token_id}, verify=False, timeout=timeout)
        except requests.exceptions.ReadTimeout:
            #logger.info("saltapi:ClientLocal, ReadTimeout! timeout: %s s" %timeout)
            return {u'return': [{}], u'status_code': 504}
        else:
            logger.info('%s "%s": %s'%(tgt, arg, ret.status_code))
            if ret.status_code == 200:
                results = ret.json()
                results['status_code'] = ret.status_code
                return results
            else:
                return {u'return': [{}], u'status_code': ret.status_code}

    def MinionStatus(self):
        params = {"client":"runner","fun":"manage.status"}
        ret = requests.post(url=self.__url, data=params, headers={'X-Auth-Token': self.__token_id}, verify=False)
        data = ret.json()
        return data['return'][0]['up'], data['return'][0]['down']

    def GetGrains(self, tgt):
        url = self.__url + '/minions/' + tgt
        ret = requests.get(url=url, headers={'X-Auth-Token': self.__token_id}, verify=False)
        data = ret.json()
        return data