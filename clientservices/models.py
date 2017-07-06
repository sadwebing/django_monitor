# coding: utf8
from django.db import models

# Create your models here.
class malfunction(models.Model):
    record_time = models.CharField(max_length=128, blank=False)
    mal_details = models.CharField(max_length=2048, blank=False)
    record_user = models.CharField(max_length=20)
    mal_reasons = models.CharField(max_length=2048)
    mal_status = models.CharField(max_length=128, default='未处理')
    recovery_time = models.CharField(max_length=128)
    time_all = models.CharField(max_length=128)
    handle_user = models.CharField(max_length=128)

class mal_history(models.Model):
	op_time = models.CharField(max_length=128, blank=False)
	op_user = models.CharField(max_length=20, blank=False)
	op_ip_addr = models.CharField(max_length=32, blank=False)
	op_type = models.CharField(max_length=64, blank=False)
	op_before = models.CharField(max_length=2048, blank=False)
	op_after = models.CharField(max_length=2048, blank=False)