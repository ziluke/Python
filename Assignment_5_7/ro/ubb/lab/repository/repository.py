import unittest

from ro.ubb.lab.domain.dictionary import My_Dict
from ro.ubb.lab.domain.entities import Student, StudentError
from ro.ubb.lab.domain.validators import StudentValidator
from ro.ubb.lab.repository.Repo_error import RepositoryError


class Repository:
    def __init__(self, validator_class):
        self.__objects = My_Dict()
        self.__validator = validator_class

    def find_by_id(self, id):
        """
        Searches by id through a dictionary
        :param id: id of the object to be searched for
        :return: the object with that id
        """
        if id not in self.__objects:
            return None
        return self.__objects[id]

    def save(self, object):
        """
        Adds a new object to the object dictionary
        :param object: object to add
        :return: nothing
        """
        self.__validator.validate(object)
        if self.find_by_id(object.id) is not None:
            raise RepositoryError("ID already taken!")
        self.__objects[object.id] = object

    def delete(self, object):
        """
        Deletes an object from the  object dictionary
        :param object: object to delete
        :return: nothing
        """
        self.__validator.validate(object)
        if object.id not in self.__objects:
            raise RepositoryError("This entity does not exist")
        del self.__objects[object.id]
        return

    def update(self, new_object):
        """
        Updates an object by overwriting the old one
        :param new_object: the new object to add
        :return: nothing
        """
        self.__validator.validate(new_object)
        if self.find_by_id(new_object.id) is None:
            raise RepositoryError("Object doesn't exist!")
        self.__objects[new_object.id] = new_object

    def get_all(self):
        """
        Returns a list of all objects
        :return: a list of all objects
        """
        return list(self.__objects.values())

    def __len__(self):
        return len(self.__objects)


class RepositoryTest(unittest.TestCase):
    def setUp(self):
        self.objects = Repository(StudentValidator)
        self.objects.save(Student(3, "Lukas", 4))
        self.objects.save(Student(2, "Victor", 6))

    def test_add(self):
        self.assertEqual(len(self.objects), 2)
        self.objects.save(Student(1, "Alex", 5))
        self.assertEqual(len(self.objects), 3)
        try:
            self.objects.save(Student("dsc", "Alex", 5))
        except StudentError:
            pass

    def test_delete(self):
        self.objects.delete(Student(3, "random", 7))
        self.assertEqual(len(self.objects), 1)
        try:
            self.objects.delete(Student(5, "random", 7))
        except RepositoryError:
            pass

    def test_update(self):
        self.objects.update(Student(3, "Alexandru", 7))
        stud = self.objects.get_all()
        self.assertEqual(stud[0].name, "Alexandru")
        self.objects.update(Student(3, "Lukas", 8))
        stud = self.objects.get_all()
        self.assertEqual(stud[0].group, 8)
        try:
            self.objects.update(Student(5, "Alexandru", 7))
        except RepositoryError:
            pass

        try:
            self.objects.update(Student("tf", "Lukas", 3))
        except StudentError:
            pass

    def test_find(self):
        stud = self.objects.find_by_id(3)
        self.assertEqual(stud, Student(3, "Lukas", 4))
        stud = self.objects.find_by_id(5)
        self.assertEqual(stud, None)

    def test_get(self):
        stud = self.objects.get_all()
        self.assertEqual(len(stud), 2)
        self.assertEqual(stud[0], Student(3, "Lukas", 4))