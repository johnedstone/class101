# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Server

class ServerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Server, ServerAdmin)

# vim: ai et ts=4 sw=4 sts=4 nu ru
