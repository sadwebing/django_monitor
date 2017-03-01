from __future__ import unicode_literals

from django.db import models

# Create your models here.
class tomcat_project(models.Model):
    product = models.CharField(max_length=10)
    project = models.CharField(max_length=64, unique=True)
    code_dir = models.CharField(max_length=32, null=True)
    tomcat = models.CharField(max_length=64, null=True)
    main_port = models.CharField(max_length=10, null=True)
    jdk = models.CharField(max_length=10, null=True)
    script = models.CharField(max_length=64, null=True)

class tomcat_url(models.Model):
    project = models.CharField(max_length=64)
    domain = models.CharField(max_length=128)
    url = models.CharField(max_length=128, unique=True)

class mail(models.Model):
    name = models.CharField(max_length=20)
    mail_address = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=20, null=True)
    role = models.CharField(max_length=10, null=True)

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
