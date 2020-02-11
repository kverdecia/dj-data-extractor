# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import (
   DataExtractor,
)


@admin.register(DataExtractor)
class DataExtractorAdmin(admin.ModelAdmin):
    pass



