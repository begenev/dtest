# -*- coding: utf-8 -*-
from datetime import datetime
import json
from django.core.exceptions import ValidationError
import os

from django.http import HttpResponse, Http404
from django.shortcuts import render

from django.conf import settings
from os.path import join
import re

import yaml
from d_test.models import TableInfo, SysFileInfo, FieldInfo, TYPE_FIELDS, TYPE_FIELD_FROM_NUMBER

def index(request):

    update_structure()

    tables = TableInfo.objects.all()

    return render(request, "index.html",  {
        'tables': tables,
        })


def update_structure():
    sys_filename = 'struct.yaml'
    fname = join(settings.PROJECT_ROOT, 'data', sys_filename)

    sys_info = SysFileInfo.objects.filter(filename=sys_filename)[:1]
    sys_info = sys_info[0] if sys_info else None

    if sys_info:
        file_modified_at = datetime.fromtimestamp(os.stat(fname).st_mtime)
        if sys_info.update_time != file_modified_at:
            # если есть данные о структуре
            f = open(fname, 'r')
            struct_data = yaml.load(f)
            f.close()

            tables = [t for t in struct_data.keys() if struct_data[t].get('title') and struct_data[t].get('fields')]
            for name in tables:
                TableInfo.objects.get_or_create(name = name, defaults={
                    'title': struct_data[name]['title']
                })

            table_fields = {tinfo.name:tinfo for tinfo in TableInfo.objects.all()}

            for name in  struct_data.keys():
                if name in table_fields:
                    position = 0
                    for field in struct_data[name].get('fields', []):
                        if field.get('id') and field.get('title') and field.get('type','') in TYPE_FIELDS:
                            field_data = {
                                'title':field['title'],
                                'type': TYPE_FIELDS[field['type']],
                                'position':position
                            }

                            obj, is_create = FieldInfo.objects.get_or_create(table = table_fields[name], name=field['id'], defaults=field_data)

                            if not is_create:
                                for k, v in field_data.items():
                                    setattr(obj, k, v)

                                obj.save()
                                print obj.name

                        position += 1

            sys_info.update_time = file_modified_at
            sys_info.save()


def ajax_edit(request):
    table_id = request.POST.get('id','') # получаем информацию - куда сохранять
    result = request.POST.get('value','')

    types_re = '|'.join(TYPE_FIELDS.keys())
    match_id = re.compile(r'^c_[1-9]\d*_\d+_\d+_('+types_re+')$')
    if not match_id.match(table_id):
        raise Http404

    names= table_id.split('_')

    try:
        table = TableInfo.objects.get(pk=names[1])
    except TableInfo.DoesNotExist:
        raise Http404

    try:
        field_name = table.fieldinfo_set.get(pk = names[3], type = TYPE_FIELDS[names[4]]).name
    except FieldInfo.DoesNotExist:
        raise Http404

    id = int(names[2])
    try:
        if id:
            obj = table.dynamic_objects.get(pk = names[2])
            setattr(obj, field_name, result)
            obj.save()
        else:
            kwargs = {field_name: result}
            obj = table.dynamic_objects.create(**kwargs)
    except (ValidationError, ValueError):
        raise Http404

    return HttpResponse(result, mimetype='text/plain')


def get_values(request):

    json_data = {}
    table_name = request.GET.get('name')
    table = None

    if table_name:
        try:
            table = TableInfo.objects.get(pk=table_name)
        except ValueError, TableInfo.DoesNotExist:
            pass

    if table:
        values = table.dynamic_objects.all().order_by('pk')
        fields_list = [{'id':f.pk,
                                'name':f.name,
                                'title':f.title,
                                'type':TYPE_FIELD_FROM_NUMBER.get(f.type,'unknown')} \
                                for f in table.fieldinfo_set.all().order_by('position') ]
        json_data['values'] = []
        values_list = []
        for v in values:
            row = []
            for f in fields_list:
                val = getattr(v, f['name'], '')
                if f['type'] == 'date' and val:
                    val = val.isoformat()

                if val is None: val = ''
                row.append(val)

            cell_data = {
                'id': v.pk,
                'row': row
            }

            values_list.append(cell_data)

        # добавляем пустые ячейки в конец таблицы
        values_list.append({
            'id': 0,
            'row':[''] * len(fields_list)
        })

        json_data.update({
            'fields': fields_list,
            'values': values_list
        })

    json_data = json.dumps(json_data, ensure_ascii=False, separators=(',',':'))
    return HttpResponse(json_data, content_type='text/plain; charset=utf-8')