# -*- coding: utf-8 -*-
'''
users:
title: Пользователи
fields:
- {id: name, title: Имя, type: char}
- {id: paycheck, title: Зарплата, type: int}
- {id: date_joined, title: Дата поступления на работу, type: date}


rooms:
title: Комнаты
fields:
- {id: department, title: Отдел, type: char}
- {id: spots, title: Вместимость, type: int}
'''

from django.db import models

class SysFileInfo(models.Model):
    filename = models.CharField(u'Название файла', max_length=64, db_index=True, unique=True)
    update_time = models.DateTimeField(u'Дата последенего изменения')


class TableInfo(models.Model):
    name = models.CharField(verbose_name=u'Имя таблицы', max_length=64)
    title = models.CharField(verbose_name=u'Заголовок таблицы', max_length=128)


TYPE_FIELDS = {
    'int':0,
    'char':1,
    'date':2
}

TYPE_FIELD_FROM_NUMBER = dict((TYPE_FIELDS[key], key) for (key, value) in TYPE_FIELDS.items())

TYPE_FIELD_CHOICES = range(0, len(TYPE_FIELDS))
for type, index in TYPE_FIELDS.items():
    TYPE_FIELD_CHOICES[index]=(index, type)

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


class EntityData(models.Model):
    row = models.IntegerField(u'Номер строки', default=0)
    field = models.ForeignKey(FieldInfo, verbose_name=u'Поле')
    int_data = models.IntegerField(u'Тип - целое число', null=True, blank=True)
    char_data = models.CharField(u'Тип - строка', max_length=1024, null=True, blank=True)
    date_data = models.DateField(u'Тип - дата', null=True, blank=True)

    class Meta:
        verbose_name = u'Значение'
        verbose_name_plural = u'Значения'

    def __unicode__(self):
        return str(self.row) + '. ' + self.field.name