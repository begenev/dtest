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
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
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

        # Adding model 'd_test_users'
        db.create_table('d_test_users', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            (u'paycheck', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            (u'date_joined', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('d_test', ['d_test_users'])

        # Adding model 'd_test_rooms'
        db.create_table('d_test_rooms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'department', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            (u'spots', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('d_test', ['d_test_rooms'])


    def backwards(self, orm):
        # Deleting model 'SysFileInfo'
        db.delete_table('d_test_sysfileinfo')

        # Deleting model 'TableInfo'
        db.delete_table('d_test_tableinfo')

        # Deleting model 'FieldInfo'
        db.delete_table('d_test_fieldinfo')

        # Deleting model 'd_test_users'
        db.delete_table('d_test_users')

        # Deleting model 'd_test_rooms'
        db.delete_table('d_test_rooms')


    models = {
        'd_test.d_test_rooms': {
            'Meta': {'object_name': 'd_test_rooms', 'db_table': "'d_test_rooms'"},
            u'department': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'spots': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'd_test.d_test_users': {
            'Meta': {'object_name': 'd_test_users', 'db_table': "'d_test_users'"},
            u'date_joined': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'paycheck': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['d_test']