#!/usr/bin/env python

"""Tests for `_template` package."""


import unittest

from _template import template
from rnx_node_editor.node_scene import Scene


class TestTemplate(unittest.TestCase):
    """Tests for `rnx_node_editor` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """test if the scene got has_been_modified property"""
        assert (hasattr(Scene, 'has_been_modified'))
