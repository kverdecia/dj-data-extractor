#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dj-data-extractor
------------

Tests for `dj-data-extractor` models module.
"""

from django.test import TestCase

from dataextractor import models


class TestDataExtractor(TestCase):

    def setUp(self):
        pass

    def test_str(self):
        extractor = models.DataExtractor()
        self.assertEqual(str(extractor), "")
        extractor.input_name="input_field"
        self.assertEqual(str(extractor), "input_field")

    def test_get_field_name(self):
        extractor = models.DataExtractor()
        self.assertEqual(extractor.get_field_name(), "")
        extractor = models.DataExtractor(input_name="input_field")
        self.assertEqual(extractor.get_field_name(), "input_field")
        extractor = models.DataExtractor(output_name="output_field")
        self.assertEqual(extractor.get_field_name(), "output_field")
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field")
        self.assertEqual(extractor.get_field_name(), "output_field")

    def test_get_value_with_omit(self):
        # when the omit attribute is True the returned value will be None
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=True, value="abc",
            expression="input_field", omit_empty=False)
        self.assertIsNone(extractor.get_value({"input_field", "123"}))
        # when the omit attribute is False the returned will be determined with the next rule
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="abc123",
            expression="input_field", omit_empty=False)
        self.assertEqual(extractor.get_value({"input_field", "123"}), "abc123")


    def tearDown(self):
        pass
