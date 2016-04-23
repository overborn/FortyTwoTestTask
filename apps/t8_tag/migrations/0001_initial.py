# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ModelLogEntry'
        db.create_table(u't8_tag_modellogentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('instance', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u't8_tag', ['ModelLogEntry'])


    def backwards(self, orm):
        # Deleting model 'ModelLogEntry'
        db.delete_table(u't8_tag_modellogentry')


    models = {
        u't8_tag.modellogentry': {
            'Meta': {'object_name': 'ModelLogEntry'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['t8_tag']