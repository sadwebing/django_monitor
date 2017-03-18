# coding: utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from monitor import settings
from check_tomcat.models import tomcat_project
from saltstack.saltapi import SaltAPI
import json, logging

logger = logging.getLogger('django')
#get saltapi url
sapi = SaltAPI(
    url      = settings.SALT_API['url'],
    username = settings.SALT_API['user'],
    password = settings.SALT_API['password']
    )

class Command(object):
    def __init__(self, tgt, fun, arg, expr_form, headers):
        self.__tgt = tgt
        self.__fun = fun
        self.__arg = arg
        self.__expr_form = expr_form
        self.__headers = headers
        self.tgt_list = []
        self.info = {}

    def TestPing(self):
        results = sapi.checkMinion(
            tgt       = self.__tgt,
            expr_form = self.__expr_form,
            )
        if self.__expr_form == 'glob':
            self.tgt_list.append(self.__tgt)
        elif self.__expr_form == 'list':
            self.tgt_list = self.__tgt
        else:
            self.tgt_list = results[0].keys()
        for minionid in self.tgt_list:
            try:
                self.info[minionid] = results[0][minionid]
            except:
                self.info[minionid] = "not return"

        return self.info

    def CmdRun(self):
        results = sapi.ClientLocal(
            tgt       = self.__tgt,
            fun       = self.__fun,
            arg       = self.__arg,
            expr_form = self.__expr_form,
            )
        #logger.info(results)
        if self.__expr_form == 'glob':
            self.tgt_list.append(self.__tgt)
        elif self.__expr_form == 'list':
            self.tgt_list = self.__tgt
        else:
            self.tgt_list = results['return'][0].keys()
        for minionid in self.tgt_list:
            try:
                self.info[minionid] = results['return'][0][minionid]
            except:
                self.info[minionid] = "not return"
        return self.info

    def StateSls(self):
        results = sapi.StateSls(
            tgt       = self.__tgt,
            fun       = self.__fun,
            arg       = self.__arg,
            expr_form = self.__expr_form,
            headers   = self.__headers
            )
        logger.info("%s: %s"%(results, dir(results)))
        #if self.__expr_form == 'glob':
        #    self.tgt_list.append(self.__tgt)
        #elif self.__expr_form == 'list':
        #    self.tgt_list = self.__tgt
        #else:
        #    self.tgt_list = results['return'][0].keys()
        #for minionid in self.tgt_list:
        #    try:
        #        self.info[minionid] = results['return'][0][minionid]
        #    except:
        #        self.info[minionid] = "not return"
        #return self.info
        return results