#!/usr/bin/python3
"""This module defines a class TestConsole"""
from console import HBNBCommand
import unittest
import sys
import io


class TestConsole(unittest.TestCase):
    """Unittest for console.py file"""

    def setUp(self):
        """This method sets up the tests"""
        self.console = HBNBCommand()

    def test_create_instance(self):
        """This test checks if an instance is created"""
        output = io.StringIO()
        sys.stdout = output
        self.console.onecmd('create State id="01234" name="California"')
        state_id = output.getvalue()
        sys.stdout = sys.__stdout__
        self.assertIn("01234", state_id)
