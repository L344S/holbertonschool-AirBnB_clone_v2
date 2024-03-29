#!/usr/bin/python3
"""This module defines a class FileStorage"""
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models import storage
import pycodestyle
import os
STORAGE_ENV = os.getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(STORAGE_ENV == "db", "no testing with FileStorage")
class test_fileStorage(unittest.TestCase):
    """Unittests for testing FileStorage class"""

    def setUp(self):
        """Method to set up the tests"""
        del_list = []
        for key in storage.all().keys():
            del_list.append(key)
        for key in del_list:
            del storage.all()[key]

    def tearDown(self):
        """Method to rename file.json back to original state"""
        try:
            os.remove('file.json')
        except BaseException:
            pass

    def test_obj_list_empty(self):
        """This test checks if __objects is empty"""
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """This test checks if new instance is created"""
        new = BaseModel()
        temp = None
        if STORAGE_ENV != "db":
            for obj in storage.all().values():
                temp = obj
        self.assertTrue(temp is None)

    def test_all(self):
        """This test checks if all() method returns the FileStorage objects"""
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ This test checks for the existence of the file"""
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ This test checks if __objects is empty """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """This file checks if file is created"""
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """This test check if reload is working"""
        new = BaseModel()
        storage.save()
        storage.reload()
        loaded = None
        for obj in storage.all().values():
            loaded = obj
        self.assertNotEqual(new, loaded)

    def test_reload_empty(self):
        """This test checks if nothing happens when file is empty"""
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """This test checks if nothing happens when file does not exist"""
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """This test checks for the existence of the file"""
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """This test checks the type of __file_path"""
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """This test checks the type of __objects"""
        self.assertEqual(type(storage.all()), dict)

    def test_storage_var_created(self):
        """This test checks for the existence of the storage"""
        from models.engine.file_storage import FileStorage
        print(type(storage))
        self.assertEqual(type(storage), FileStorage)


class TestFileStoragePEP8(unittest.TestCase):
    """This class will test pycodestyle style"""

    def test_pep8(self):
        """This test will check for pycodestyle validation"""
        pep8style = pycodestyle.StyleGuide(quiet=True)
        result = pep8style.check_files(["models/engine/file_storage.py"])
        self.assertEqual(result.total_errors, 0, "pycodestyle failed")

    def test_docs(self):
        """This test will check for documentation"""
        self.assertIsNotNone(FileStorage.__doc__)
