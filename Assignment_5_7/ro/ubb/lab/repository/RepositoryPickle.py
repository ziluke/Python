import pickle

from ro.ubb.lab.domain.dictionary import My_Dict
from ro.ubb.lab.repository.Repo_error import RepositoryError


class RepositoryPickle:
    def __init__(self, f_name, validator_class, entity):
        self.__f_name = f_name
        self.__validator = validator_class
        self.__entity = entity

    def find_by_id(self, id):
        """
        Searches by id through a dictionary
        :param id: id of the object to be searched for
        :return: the object with that id
        """
        objects = self.__get_all()
        if id not in objects:
            return None
        return objects[id]

    def save(self, object):
        """
        Adds a new object to the object dictionary
        :param object: object to add
        :return: nothing
        """
        self.__validator.validate(object)
        file = open(self.__f_name, "ab")
        if self.find_by_id(object.id) is not None:
            raise RepositoryError("Id already taken!")
        pickle.dump(object, file)
        file.close()

    def delete(self, object):
        """
        Deletes an object from the  object dictionary
        :param object: object to delete
        :return: nothing
        """
        self.__validator.validate(object)
        if self.find_by_id(object.id) is not None:
            objects = self.__get_all()
            del objects[object.id]
        else:
            raise RepositoryError("This entity does not exist")
        self.overwrite(objects)

    def update(self, new_object):
        """
        Updates an object by overwriting the old one
        :param new_object: the new object to add
        :return: nothing
        """
        self.__validator.validate(new_object)
        if self.find_by_id(new_object.id) is None:
            raise RepositoryError("Object doesn't exist!")
        objects = self.__get_all()
        objects[new_object.id] = new_object
        self.overwrite(objects)

    def overwrite(self, objects):
        file = open(self.__f_name, "wb")
        for object in objects.values():
            pickle.dump(object, file)
        file.close()

    def get_all(self):
        """
        Returns a list of all objects
        :return: a list of all objects
        """
        return list(self.__get_all().values())

    def __get_all(self):
        objects = My_Dict()
        try:
            file = open(self.__f_name, "rb")
            while True:
                try:
                    object = pickle.load(file)
                    objects[object.id] = object
                except EOFError:
                    break
        except EOFError:
            raise RepositoryError("File is empty!")
        except IOError:
            raise RepositoryError("Invalid file!")
        file.close()
        return objects
