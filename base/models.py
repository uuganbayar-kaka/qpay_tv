import json
from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField

from django.db import models
from django.db.models import F
from django.contrib.postgres.fields import JSONField
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.postgres.fields import ArrayField
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Invoice(models.Model):

    id = models.UUIDField(default=id, editable=False)
    description = models.CharField("description", max_length=100, blank=True, null=True)
    invoice_id = models.CharField("invoice_id", max_length=100, blank=True, null=True)
    invoice_data = models.CharField("invoice_data", max_length=100, blank=True, null=True)
    amount = models.CharField("amount", max_length=100, blank=True, null=True)
    expire_date = models.CharField("expire_date", max_length=100, blank=True, null=True)
    created_by = models.CharField("created_by", max_length=100, blank=True, null=True)
    created_date = models.DateTimeField("Date Time")
    updated_by = models.CharField("updated_by", max_length=100, blank=True, null=True)
    updated_date = models.DateTimeField("Date Time", null=True, blank=True)
    invoice_status_code = models.CharField("invoice_status_code", max_length=100, blank=True, null=True)
    status = models.CharField("status", max_length=100, blank=True, null=True)

    response_invoice_id = models.CharField("response_invoice_id", max_length=100, blank=True, null=True)
    qr_short_url = models.CharField("qr_short_url", max_length=100, blank=True, null=True)
    qr_text = models.CharField("qr_text", max_length=100, blank=True, null=True)
    qr_image = models.TextField("HTML")

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoice"
        managed = False
        db_table = 'invoice'

    def __unicode__(self):
        return "%s" % (self.invoice_id)

    def __str__(self):
        return "%s" % (self.invoice_id)

    def to_json(self):
        json_data = {
            'id': self.id,
            'description': self.description,
            'invoice_data': self.invoice_data,
            'amount': self.amount,
            'invoice_id': self.invoice_id,
            'expire_date': self.expire_date,
            'created_by': self.created_by,
            'created_date': self.created_date,
            'updated_by': self.updated_by,
            'updated_date': self.updated_date,
            'invoice_status_code': self.invoice_status_code,
            'status': self.status,
            'response_invoice_id':self.response_invoice_id,
            'qr_short_url':self.qr_short_url,
            'qr_text':self.qr_text,
            'qr_image':self.qr_image,
        }

        return json_data
