# coding: utf8
from django.db import models

# Create your models here.
class malfunction(models.Model):
    record_time = models.CharField(max_length=128, blank=False)
    mal_details = models.CharField(max_length=2048, blank=False)
    record_user = models.CharField(max_length=128)
    mal_reasons = models.CharField(max_length=2048)
    mal_status = models.CharField(max_length=128, default='未处理')
    recovery_time = models.CharField(max_length=128)
    time_all = models.CharField(max_length=128)
    handle_user = models.CharField(max_length=128)