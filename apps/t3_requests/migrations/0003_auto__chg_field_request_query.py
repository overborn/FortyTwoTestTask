# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Request.query'
        db.alter_column(u't3_requests_request', 'query', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

    def backwards(self, orm):

        # Changing field 'Request.query'
        db.alter_column(u't3_requests_request', 'query', self.gf('django.db.models.fields.CharField')(default='', max_length=256))

    models = {
        u't3_requests.request': {
            'Meta': {'object_name': 'Request'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['t3_requests']