import unittest

from ro.ubb.lab.domain.entities import Student, StudentValidator, StudentError
from ro.ubb.lab.operations.undo.handlers import UndoHandler
from ro.ubb.lab.operations.undo.manager import UndoManager
from ro.ubb.lab.repository.repository import Repository
from ro.ubb.lab.repository.Repo_error import RepositoryError


class StudentService:
    def __init__(self, repository):
        self.__repository = repository

    def add_student(self, id, name, group):
        """
        Adds a new student
        :param id: student id
        :param name: student name
        :param group: student group
        :return: nothing
        """
        self.__repository.save(Student(id, name, group))

        UndoManager.register_operation(self.__repository, UndoHandler.ADD_STUDENT, Student(id, name, group))

    def delete_student(self, id):
        """
        Deletes a student
        :param id: the id of the student
        :return: nothing
        """
        UndoManager.register_operation(self.__repository, UndoHandler.DELETE_STUDENT, self.find_student(id),
                                       "delete_student")
        self.__repository.delete(Student(id, "random", 0))

    def update_student(self, id, arg=None, group=None):
        """
        Updates the name and/or group of the student
        :param id: student id
        :param arg: new name/ new group
        :param group: new group
        :return: nothing
        """
        student = self.find_student(id)
        try:
            arg = int(arg)
            if group is None:
                UndoManager.register_operation(self.__repository, UndoHandler.UPDATE_STUDENT, student, "update_student")
                self.__repository.update(Student(id, student.name, arg))
        except ValueError:
            if group is None:
                UndoManager.register_operation(self.__repository, UndoHandler.UPDATE_STUDENT, student, "update_student")
                self.__repository.update(Student(id, arg, student.group))
            else:
                UndoManager.register_operation(self.__repository, UndoHandler.UPDATE_STUDENT, student, "update_student")
                self.__repository.update(Student(id, arg, group))

    def find_student(self, id):
        """
        Searches for a student in the student dictionary
        :param id: student id
        :return: the student object if it is found, else None
        """
        return self.__repository.find_by_id(id)

    def get_all_students(self):
        """
        Returns a list of all students
        :return: the list of all students
        """
        return self.__repository.get_all()

    def __len__(self):
        return len(self.__repository)


class StudentServiceTest(unittest.TestCase):
    def setUp(self):
        self.students = StudentService(Repository(StudentValidator))
        self.students.add_student(4, "Lukas", 4)
        self.students.add_student(2, "Victor", 7)

    def test_add(self):
        self.assertEqual(len(self.students), 2)
        self.students.add_student(3, "Alex", 5)
        self.assertEqual(len(self.students), 3)
        try:
            self.students.add_student("dsc", "Alex", 5)
        except StudentError:
            pass

    def test_delete(self):
        self.students.delete_student(4)
        self.assertEqual(len(self.students), 1)
        try:
            self.students.delete_student(5)
        except RepositoryError:
            pass

    def test_update(self):
        self.students.update_student(2, "Alexandru", 7)
        stud = self.students.get_all_students()
        self.assertEqual(stud[1].name, "Alexandru")
        self.students.update_student(4, "Lukas", 8)
        stud = self.students.get_all_students()
        self.assertEqual(stud[0].group, 8)
        try:
            self.students.update_student(5, "Alexandru", 7)
        except RepositoryError:
            pass

        try:
            self.students.update_student("tf", "Lukas", 3)
        except StudentError:
            pass

    def test_find(self):
        stud = self.students.find_student(4)
        self.assertEqual(stud, Student(4, "Lukas", 4))
        stud = self.students.find_student(5)
        self.assertEqual(stud, None)

    def test_get(self):
        stud = self.students.get_all_students()
        self.assertEqual(len(stud), 2)
        self.assertEqual(stud[0], Student(4, "Lukas", 4))
