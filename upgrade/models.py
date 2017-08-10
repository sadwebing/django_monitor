# coding: utf-8
from django.db import models

# Create your models here.

class upgrade_op(models.Model):
    svn_id = models.CharField(max_length=20, blank=False)
    id_time = models.CharField(max_length=32, blank=False)
    project = models.CharField(max_length=64)
    cur_status = models.CharField(max_length=16)
    op_time = models.CharField(max_length=64)
    handle_user = models.CharField(max_length=64)

class upgrade_cur_svn(models.Model):
	product = models.CharField(max_length=10)
	project = models.CharField(max_length=64, unique=True)
	cur_svn_id = models.CharField(max_length=20)
	class Meta:
		unique_together = ('product', 'project')

class svn_id(models.Model):
    id_time = models.CharField(max_length=32, blank=False)
    svn_id = models.CharField(max_length=32, blank=False)
    tag = models.CharField(max_length=32, blank=True)
    project = models.CharField(max_length=64, unique=False)
    envir_uat = models.CharField(max_length=16, default='undone')
    envir_online = models.CharField(max_length=16, default='undone')
    deleted = models.IntegerField(default=0)
    lock = models.IntegerField(default=0)
    info = models.CharField(max_length=128, blank=True)
    class Meta:
        unique_together = ('svn_id', 'project')

class op_history(models.Model):
    svn_id = models.CharField(max_length=20, blank=False)
    project = models.CharField(max_length=128)
    ip_addr = models.GenericIPAddressField(blank=False)
    act = models.CharField(max_length=20, blank=False)
    op_time = models.CharField(max_length=64, blank=False)
    op_user = models.CharField(max_length=64, blank=False)
    op_ip_addr = models.GenericIPAddressField(blank=False)
    op_status = models.IntegerField(default=0)
    envir = models.CharField(max_length=10)
    info = models.TextField(max_length=51200, blank=True)