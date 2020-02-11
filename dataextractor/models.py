# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from collections import OrderedDict
# from django.utils.six import python_2_unicode_compatible
from django.db import models
from django.utils.translation import ugettext_lazy as _


# @python_2_unicode_compatible
class DataExtractor(models.Model):
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
        if not self.output_name:
            self.output_name = self.input_name
        return super(DataTranslator, self).save(*args, **kwargs)

    def get_field_name(self):
        return self.output_name or self.input_name

    def get_value(self, data):
        if self.omit:
            return None
        if self.value:
            return self.value
        if self.expression:
            return None
        return data.get(self.input_name)

    def get_object(self, data):
        pass
