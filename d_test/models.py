# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from django.db import models


class SysFileInfo(models.Model):
    filename = models.CharField(u'Название файла', max_length=64, db_index=True, unique=True)
    update_time = models.DateTimeField(u'Дата последенего изменения')

TYPE_FIELDS = {
    'int':0,
    'char':1,
    'date':2
}

TYPE_FIELD_FROM_NUMBER = dict((TYPE_FIELDS[key], key) for (key, value) in TYPE_FIELDS.items())

TYPE_FIELD_CHOICES = range(0, len(TYPE_FIELDS))
for t, index in TYPE_FIELDS.items():
    TYPE_FIELD_CHOICES[index]=(index, t)

class TableInfo(models.Model):
    name = models.CharField(verbose_name=u'Имя таблицы', max_length=64, unique=True)
    title = models.CharField(verbose_name=u'Заголовок таблицы', max_length=128)

    def _get_field_list(self):
        fields = []
        for field in self.fieldinfo_set.all().order_by('position'):
            fields.append(
                    {
                    'id': field.name,
                    'title': field.title,
                    'type': TYPE_FIELD_FROM_NUMBER[field.type],
                    }
            )
        return fields

    def _get_meta_opts(self):
        return {
            'verbose_name': self.title.capitalize() if self.title else self.name
        }

    @property
    def dynamic_class(self):
        return CommonModel(str(self.name), self._get_field_list(), self._get_meta_opts())

    @property
    def dynamic_objects(self):
        return self.dynamic_class.objects

    def synced_model(self):
        return self.dynamic_class._model

class FieldInfo(models.Model):

    TYPE_CHOICES = TYPE_FIELD_CHOICES

    table = models.ForeignKey(TableInfo, verbose_name=u'Относится к таблице', name='fields')
    name = models.CharField(u'Имя поля', max_length=64, db_index=True)
    title = models.CharField(u'Заголовок поля', max_length=128)
    type = models.IntegerField(u'Тип поля', choices=TYPE_FIELD_CHOICES, db_index=True)
    position = models.IntegerField(u'Порядок вывода', default=0)

    class Meta:
        verbose_name = u'Поле'
        verbose_name_plural = u'Поля'

    def __unicode__(self):
        return self.table.name + '.' + self.name


class CommonModel(object):

    def __init__(self, name, fields, meta_opts={}):
        '''
        fields передается как список словарей вида,
        все ключи у словарей должны быть обязательно:
        [{'id': 'name', 'title': u'Имя', 'type': 'char'}, ...]
        '''

        self._name = name
        self._app_name = 'd_test'
        self._meta_opts = {
            'verbose_name': self._name.capitalize()
        }
        self._meta_opts.update(meta_opts)
        self._fields = {
        }
        for fld in fields:
            self._fields[fld['id']] = self._str_to_field(fld['type'], fld['title'])

        self._admin_opts = {}
        self._model = self._create_model()

    def _str_to_field(self, type_name, title):
        STR_TYPE_FROM_FIELDS = {
            'int':models.IntegerField(verbose_name=title, null=True, blank=True),
            'char':models.CharField(verbose_name=title, max_length=128, null=True, blank=True),
            'date':models.DateField(verbose_name=title, null=True, blank=True),
            }
        return STR_TYPE_FROM_FIELDS[type_name]

    def _create_model(self):

        table_name = '%s_%s' % (self._app_name, self._name)

        class Meta:
            app_label = self._app_name
            db_table = table_name

        for key, value in self._meta_opts.iteritems():
            setattr(Meta, key, value)

        attrs = {'__module__': self.__class__.__module__,
                 'Meta' : Meta,
                 'objects' : models.Manager()}

        attrs.update(self._fields)

        return type(table_name, (models.Model,), attrs)

    @property
    def objects(self):
        return self._model.objects.get_query_set()

tables = TableInfo.objects.all()

if tables:
    site = admin.site

    for table in tables:

        model = table.synced_model()

        for reg_model in site._registry.keys():
            if model._meta.db_table == reg_model._meta.db_table:
                del site._registry[reg_model]

        try:
            site.unregister(model)
        except NotRegistered:
            pass


        class Admin(admin.ModelAdmin):
            pass

        admin.site.register(model, Admin)