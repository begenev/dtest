# -*- coding: utf-8 -*-

from django.contrib import admin
from d_test.models import SysFileInfo, EntityData

class SysFileInfoAdmin(admin.ModelAdmin):
    pass

class EntityDataAdmin(admin.ModelAdmin):
    pass

admin.site.register(SysFileInfo, SysFileInfoAdmin)

admin.site.register(EntityData, EntityDataAdmin)