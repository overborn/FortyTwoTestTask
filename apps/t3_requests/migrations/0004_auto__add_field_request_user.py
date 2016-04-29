# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Request.user'
        db.add_column(u't3_requests_request', 'user',
                      self.gf('django.db.models.fields.CharField')(default='anonymous', max_length=30),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Request.user'
        db.delete_column(u't3_requests_request', 'user')


    models = {
        u't3_requests.request': {
            'Meta': {'object_name': 'Request'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'default': "'anonymous'", 'max_length': '30'})
        }
    }

    complete_apps = ['t3_requests']