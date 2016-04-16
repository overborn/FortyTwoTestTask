# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Request'
        db.create_table(u't3_requests_request', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('query', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u't3_requests', ['Request'])


    def backwards(self, orm):
        # Deleting model 'Request'
        db.delete_table(u't3_requests_request')


    models = {
        u't3_requests.request': {
            'Meta': {'object_name': 'Request'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['t3_requests']