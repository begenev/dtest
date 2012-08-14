# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SysFileInfo'
        db.create_table('d_test_sysfileinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, db_index=True)),
            ('update_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('d_test', ['SysFileInfo'])

        # Adding model 'TableInfo'
        db.create_table('d_test_tableinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('d_test', ['TableInfo'])

        # Adding model 'FieldInfo'
        db.create_table('d_test_fieldinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['d_test.TableInfo'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('type', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('d_test', ['FieldInfo'])

        # Adding model 'EntityData'
        db.create_table('d_test_entitydata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('row', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['d_test.FieldInfo'])),
            ('int_data', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('char_data', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('date_data', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('d_test', ['EntityData'])


    def backwards(self, orm):
        # Deleting model 'SysFileInfo'
        db.delete_table('d_test_sysfileinfo')

        # Deleting model 'TableInfo'
        db.delete_table('d_test_tableinfo')

        # Deleting model 'FieldInfo'
        db.delete_table('d_test_fieldinfo')

        # Deleting model 'EntityData'
        db.delete_table('d_test_entitydata')


    models = {
        'd_test.entitydata': {
            'Meta': {'object_name': 'EntityData'},
            'char_data': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'date_data': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['d_test.FieldInfo']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'int_data': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'row': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'd_test.fieldinfo': {
            'Meta': {'object_name': 'FieldInfo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['d_test.TableInfo']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'd_test.sysfileinfo': {
            'Meta': {'object_name': 'SysFileInfo'},
            'filename': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'd_test.tableinfo': {
            'Meta': {'object_name': 'TableInfo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['d_test']