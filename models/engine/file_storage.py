#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of all objects of a certain class
        or all objects if no class is specified"""
        if cls:
            actual_dict = {}
            # loop through all objects in __objects
            for key, value in FileStorage.__objects.items():
                # if the class of the object is the same as the class
                if cls == value.__class__:
                    actual_dict[key] = value
            return actual_dict
        # if no class is specified, return all objects
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        # open file.json in write mode
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            # copy all objects in __objects to temp
            temp.update(FileStorage.__objects)
            # convert all objects in temp to dictionary format
            for key, val in temp.items():
                temp[key] = val.to_dict()
            # write temp to file.json
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            temp = {}
            # open file.json in read mode
            with open(FileStorage.__file_path, 'r') as f:
                # load data from file.json into temp
                temp = json.load(f)
                # for each key, val in temp create an object in __objects
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """If obj is not None, deletes obj from __objects"""
        if not obj:
            return
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        # if key exists in __objects, delete it
        if key in self.__objects:
            del self.__objects[key]
        # save the changes
        self.save()
