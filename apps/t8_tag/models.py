# -*- coding: utf-8 -*-
from django.db import models


class ModelLogEntry(models.Model):
    model = models.CharField(max_length=30)
    instance = models.CharField(max_length=40)
    action = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"[{}] {} {}: {}".format(
            self.created.strftime('%Y-%m-%d %H:%M:%S'),
            self.action,
            self.model,
            self.instance
        )
