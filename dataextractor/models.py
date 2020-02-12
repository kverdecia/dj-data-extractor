# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict
import jmespath
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .functions import Functions


class DataExtractor(models.Model):
    "Abstract model defining rules for extracting data from dicts."
    input_name = models.CharField(_("Input name"), max_length=60)
    output_name = models.CharField(_("Field name"), max_length=60, blank=True, default='')
    omit = models.BooleanField(_("Omit"), blank=True, default=False)
    value = models.TextField(_("Default value"), blank=True, default='')
    expression = models.CharField(_("Expression"), max_length=250, blank=True, default='')
    omit_empty = models.BooleanField(_("Exclude if empty"), blank=True, default=False)

    class Meta:
        abstract = True
        verbose_name = _("Data extractor")
        verbose_name_plural = _("Data extractors")

    def __str__(self):
        return self.input_name

    def save(self, *args, **kwargs):
        "Before save if output_name is empty assigns the value of input_name."
        if not self.output_name:
            self.output_name = self.input_name
        return super(DataExtractor, self).save(*args, **kwargs)

    def get_field_name(self):
        "Returns the name of the output field."
        return self.output_name or self.input_name

    def get_value(self, data):
        "Extracts data from a data dict."
        if self.omit:
            return None
        if self.value:
            return self.value
        if self.expression:
            options = jmespath.Options(custom_functions=Functions())
            return jmespath.search(self.expression, data, options=options)
        return data.get(self.input_name)

    def get_data(self, data):
        "extracts an ordered dict from data parameter."
        if self.omit:
            return OrderedDict()
        value = self.get_value(data)
        if self.omit_empty and value is None:
            return OrderedDict()
        return OrderedDict([[self.get_field_name(), value]])
