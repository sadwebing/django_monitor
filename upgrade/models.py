# coding: utf-8
from django.db import models

# Create your models here.

class upgrade_op(models.Model):
    svn_id = models.CharField(max_length=20, blank=False)
    id_time = models.CharField(max_length=64, blank=False)
    project = models.CharField(max_length=64)
    cur_status = models.CharField(max_length=16)
    op_time = models.CharField(max_length=64)
    handle_user = models.CharField(max_length=64)

#class upgrade_op_history(models.Model):
#    svn_id = models.CharField(max_length=20, blank=False)
#    id_time = models.CharField(max_length=64, blank=False)
#    project = models.CharField(max_length=128)
#    cur_status = models.CharField(max_length=16)
#    op_time = models.CharField(max_length=64)
#    handle_user = models.CharField(max_length=64)