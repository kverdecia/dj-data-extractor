#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dj-data-extractor
------------

Tests for `dj-data-extractor` models module.
"""

import datetime
from collections import OrderedDict
from django.test import TestCase
from dataextractor import models


class TestDataExtractor(TestCase):

    def setUp(self):
        pass

    def test_str(self):
        "test the conversion to str returns the value of input_name attr."
        extractor = models.DataExtractor()
        self.assertEqual(str(extractor), "")
        extractor.input_name = "input_field"
        self.assertEqual(str(extractor), "input_field")

    def test_get_field_name(self):
        "test the get_field_name method"
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
        "when the omit attribute is True the returned value will be None"
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=True, value="abc",
            expression="input_field", omit_empty=False)
        self.assertIsNone(extractor.get_value({"input_field", "123"}))

    def test_get_value_with_value(self):
        "if omit attr is False and value attr is not empty returns the value attr"
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="abc123",
            expression="input_field", omit_empty=False)
        self.assertEqual(extractor.get_value({"input_field", "123"}), "abc123")

    def test_get_value_with_expression(self):
        "if not omit and value attrs then use expression attr to extract the data"
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="",
            expression="foo.bar[0]", omit_empty=True)
        data = {"foo": {"bar": [{"name": "one"}, {"name": "two"}]}}
        self.assertEqual(extractor.get_value(data), {"name": "one"})
        # If cannot find the expression the result is None
        extractor2 = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="",
            expression="foo.baz[0]", omit_empty=True)
        self.assertEqual(extractor2.get_value(data), None)
        # test nul in the expression
        extractor3 = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="",
            expression="`null`", omit_empty=True)
        self.assertEqual(extractor3.get_value(data), None)
        # test a value in the expression
        extractor4 = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="",
            expression="`33`", omit_empty=True)
        self.assertEqual(extractor4.get_value(data), 33)

    def test_custom_function_date(self):
        "test custom function date"
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="",
            expression="foo.date | date(@, '%Y-%m-%d')", omit_empty=True)
        data = {"foo": {"date": "1998-12-23"}}
        date = datetime.date(1998, 12, 23)
        self.assertEqual(extractor.get_value(data), date)

    def test_custom_function_time(self):
        "test custom function time"
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="",
            expression="foo.time | time(@, '%H:%M:%S')", omit_empty=True)
        data = {"foo": {"time": "23:45:54"}}
        time = datetime.time(23, 45, 54)
        self.assertEqual(extractor.get_value(data), time)

    def test_custom_function_datetime(self):
        "test custom function datetime"
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="",
            expression="foo.datetime | datetime(@, '%Y-%m-%dT%H:%M:%S')", omit_empty=True)
        data = {"foo": {"datetime": "1998-12-23T23:45:54"}}
        date = datetime.datetime(1998, 12, 23, 23, 45, 54)
        self.assertEqual(extractor.get_value(data), date)

    def test_custom_function_format(self):
        "test custom function format"
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="",
            expression="foo.datetime | format(@, '%d/%m/%Y')", omit_empty=True)
        data = {"foo": {"datetime": datetime.datetime(1998, 12, 23, 23, 45, 54)}}
        self.assertEqual(extractor.get_value(data), "23/12/1998")

    def test_custom_function_if(self):
        "test custom function if"
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="",
            expression="if(`true`, `3`, `6`)", omit_empty=True)
        self.assertEqual(extractor.get_value({}), 3)
        extractor2 = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="",
            expression="if(`false`, `3`, `6`)", omit_empty=True)
        self.assertEqual(extractor2.get_value({}), 6)

    def test_custom_function_json(self):
        extractor = models.DataExtractor(input_name="input_fields",
            expression="value | json(@)")
        data = {"value": '{"item": "abc"}'}
        self.assertEqual(extractor.get_value(data), {'item': 'abc'})
        extractor2 = models.DataExtractor(input_name="input_fields",
            expression="value | json(@) | item")
        self.assertEqual(extractor2.get_value(data), "abc")

    def test_get_data_with_omit(self):
        "if omit attr is True returns an empty ordered dict."
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=True, value="abc",
            expression="input_field", omit_empty=False)
        self.assertEqual(extractor.get_data({"input_field", "123"}), OrderedDict())

    def test_get_data_without_output_name(self):
        "when output_name attr is empty, the result key will be the value in input_name"
        extractor = models.DataExtractor(input_name="input_field",
            output_name="", omit=False, value="abc",
            expression="input_field", omit_empty=False)
        result = OrderedDict([["input_field", "abc"]])
        self.assertEqual(extractor.get_data({"input_field", "123"}), result)

    def test_get_data_with_output_name(self):
        "when output_name attr is empty, the result key will be the value in input_name"
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="abc",
            expression="input_field", omit_empty=False)
        result = OrderedDict([["output_field", "abc"]])
        self.assertEqual(extractor.get_data({"input_field", "123"}), result)

    def test_get_data_without_omit_empty(self):
        "when omit_empty attr is False and result value is None, the key and the value will be in the result."
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="",
            expression="`null`", omit_empty=False)
        result = OrderedDict([["output_field", None]])
        self.assertEqual(extractor.get_data({}), result)

    def test_get_data_with_omit_empty(self):
        "when omit_empty attr is True and result vale is None, the result will be an empty ordered dict."
        extractor = models.DataExtractor(input_name="input_field",
            output_name="output_field", omit=False, value="",
            expression="`null`", omit_empty=True)
        self.assertEqual(extractor.get_data({}), OrderedDict())

    def test_merge_data_extractors(self):
        "test data extracted from diferent extractors."
        extractor1 = models.DataExtractor(input_name="value1", output_name="value_a")
        extractor2 = models.DataExtractor(input_name="value2", output_name="value_b")
        data = {
            'value1': 1,
            'value2': 2,
        }
        output = OrderedDict([['value_a', 1], ['value_b', 2]])
        self.assertEqual(models.DataExtractor.merge_data_extractors([extractor1, extractor2], data), 
            output)

    def test_merge_data_extractors_override(self):
        "test data extracted from diferent extractors. overriding"
        extractor1 = models.DataExtractor(input_name="value1", output_name="value_a")
        extractor2 = models.DataExtractor(input_name="value2", output_name="value_b")
        extractor3 = models.DataExtractor(input_name="value1", output_name="value_b")
        data = {
            'value1': 1,
            'value2': 2,
        }
        output = OrderedDict([['value_a', 1], ['value_b', 1]])
        extractors = [extractor1, extractor2, extractor3]
        self.assertEqual(models.DataExtractor.merge_data_extractors(extractors, data), 
            output)

    def tearDown(self):
        pass
