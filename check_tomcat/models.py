from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class tomcat_project(models.Model):
    product = models.CharField(max_length=10)
    project = models.CharField(max_length=64, unique=True)
    server_type = models.CharField(max_length=10, default='tomcat')
    code_dir = models.CharField(max_length=32, null=True)
    cur_svn_id = models.CharField(max_length=20)
    tomcat = models.CharField(max_length=64, null=True)
    tomcat_version = models.CharField(max_length=10, null=True, default='7')
    main_port = models.CharField(max_length=10, null=True)
    jdk = models.CharField(max_length=10, null=True)
    script = models.CharField(max_length=64, null=True)
    status = models.CharField(max_length=10, null=True,  default='active')
    class Meta:
        unique_together = ('product', 'project')

class tomcat_url(models.Model):
    envir = models.CharField(max_length=10, default='ONLINE')
    project = models.CharField(max_length=64)
    minion_id = models.CharField(max_length=32, null=True)
    ip_addr = models.CharField(max_length=32, null=True)
    server_type = models.CharField(max_length=10, default='tomcat')
    role = models.CharField(max_length=16, default='backup')
    domain = models.CharField(max_length=128)
    url = models.CharField(max_length=128, null=True)
    status = models.CharField(max_length=20, default='active')
    info = models.CharField(max_length=128, null=True)
    class Meta:
        unique_together = ('project', 'minion_id')

class mail(models.Model):
    name = models.CharField(max_length=20)
    mail_address = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=20, null=True)
    role = models.CharField(max_length=10, null=True)
    check_services = models.IntegerField(default=0)
    check_salt_minion = models.IntegerField(default=0)

class tomcat_status(models.Model):
    access_time = models.CharField(max_length=64)
    project = models.CharField(max_length=64)
    domain = models.CharField(max_length=128)
    url = models.CharField(max_length=128)
    code = models.CharField(max_length=8)
    info = models.CharField(max_length=1024, null=True)

class server_status(models.Model):
    access_time = models.CharField(max_length=64)
    url = models.CharField(max_length=128)
    status = models.CharField(max_length=10, null=True)
    info = models.CharField(max_length=1024, null=True)

class check_status(models.Model):
    program = models.CharField(max_length=32)
    status = models.IntegerField(default=0)
