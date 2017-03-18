# -*- coding: utf-8 -*-

import requests,json

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

    def ClientLocal(self, tgt, fun, arg, expr_form='list', headers={}):
        if tgt == '*':
            params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        else:
            params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        ret = requests.post(url=self.__url, data=params, headers=dict({'X-Auth-Token': self.__token_id}, **headers), verify=False)
        return ret.json()

    def StateSls(self, tgt, fun, arg, expr_form='list', headers={}):
        if tgt == '*':
            params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        else:
            params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        ret = requests.post(url=self.__url, data=params, headers=dict({'X-Auth-Token': self.__token_id}, **headers), verify=False)
        return ret.text()

    def MinionStatus(self):
        params = {"client":"runner","fun":"manage.status"}
        ret = requests.post(url=self.__url, data=params, headers={'X-Auth-Token': self.__token_id}, verify=False)
        data = ret.json()
        return data['return'][0]['up'], data['return'][0]['down']
