#!/usr/bin/python3
"""This module defines test cases for DBStorage class"""
import unittest
from models import storage
from models.engine.db_storage import DBStorage
import pycodestyle
from os import getenv
STORAGE_ENV = getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(STORAGE_ENV != "db", "no testing with db storage")
class TestDBStorage(unittest.TestCase):
    """Unittests for testing DBStorage class"""

    def setUp(self):
        """Method to set up the tests"""
        del_list = []
        for key in storage.all().keys():
            del_list.append(key)
        for key in del_list:
            storage._DBStorage__session.delete(storage.all()[key])
            storage._DBStorage__session.commit()

    def test_storage_instance(self):
        """This test checks for the existence of the DBStorage instance"""
        self.assertEqual(type(storage), DBStorage)

    def test_all(self):
        """This test checks if all() method returns the FileStorage objects"""
        self.assertEqual(type(storage.all()), dict)

    def test_empty_db(self):
        """This test checks if the database is empty"""
        self.assertEqual(len(storage.all()), 0)

    def test_storage(self):
        """This test checks for the existence of the storage"""
        from models.state import State
        new = State(name="California")
        new.save()
        objId = new.to_dict()['id']
        self.assertIn(new.__class__.__name__ + '.' + objId,
                      storage.all(type(new)).keys())


class TestDBStoragePEP8(unittest.TestCase):
    """This class will test pycodestyle style"""

    def test_pep8(self):
        """This test will check for pycodestyle validation"""
        pep8style = pycodestyle.StyleGuide(quiet=True)
        result = pep8style.check_files(["models/engine/db_storage.py"])
        self.assertEqual(result.total_errors, 0, "pycodestyle failed")

    def test_docs(self):
        """This test will check for documentation"""
        self.assertIsNotNone(DBStorage.__doc__)
