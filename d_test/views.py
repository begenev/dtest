# -*- coding: utf-8 -*-
from datetime import datetime
import json
from django.core.exceptions import ValidationError
import os

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, render
from django.template import RequestContext

from django.conf import settings
from os.path import join
import re

import yaml
from d_test.models import TableInfo, SysFileInfo, FieldInfo, TYPE_FIELDS, EntityData, TYPE_FIELD_FROM_NUMBER

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
    match_id = re.compile(r'^cell_\d+_\d+_('+types_re+')$')
    if not match_id.match(table_id):
        raise Http404

    names= table_id.split('_')

    field = FieldInfo.objects.all()

    try:
        field = FieldInfo.objects.get(pk=names[2])
    except FieldInfo.DoesNotExist:
        raise Http404

    if field:
        try:
            obj, is_created = EntityData.objects.get_or_create(
                field=field,
                row=names[1],
                defaults={
                    names[3]+'_data':result
                })

            if not is_created:
                setattr(obj, names[3]+'_data', result)
                obj.save()
        except ValueError:
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
        json_data['fields'] = [{'id':f.pk,
                                'title':f.title,
                                'type':TYPE_FIELD_FROM_NUMBER.get(f.type,'unknown')} \
                                for f in FieldInfo.objects.filter(table = table).order_by('position') ]
        json_data['values'] = []
        values = EntityData.objects.filter(field__table=table).\
                order_by( 'field__position')

        values_dict = {}
        row = []
        for v in values:
            type_data = TYPE_FIELD_FROM_NUMBER.get(v.field.type,'unknown')
            cell_data = {
                'value':getattr(v, '%s_data' % type_data),
                'fid': v.field.pk,
                'row': v.row
            }
            if type_data == 'date' and cell_data['value']:
                cell_data['value'] = cell_data['value'].isoformat()


            if v.row in values_dict:
                values_dict[v.row].append(cell_data)
            else:
                values_dict[v.row] = [cell_data]

        # добавляем пустые ячейки в конец таблицы
        max_row = max(values_dict.keys()) + 1 if values_dict else 0
        values_dict[max_row] = []
        for field in json_data['fields']:
            values_dict[max_row].append({
                'value':'',
                'fid': field['id'],
                'row': max_row
            })

        sorted(values_dict)
        json_data['values'] = values_dict.values()

    json_data = json.dumps(json_data, ensure_ascii=False, separators=(',',':'))
    return HttpResponse(json_data, content_type='text/plain; charset=utf-8')