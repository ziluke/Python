import unittest

from ro.ubb.lab.domain.entities import Grade, GradeValidator, GradeError, Student
from ro.ubb.lab.operations.undo.handlers import UndoHandler
from ro.ubb.lab.operations.undo.manager import UndoManager
from ro.ubb.lab.repository.repository import Repository, RepositoryError


class GradeService:
    def __init__(self, repository):
        self.__repository = repository

    def find_grade(self, assID, studID):
        """
        Returns the grade object/ None if the student has/has not assignment
        :param assID: assignment id
        :param studID: student id
        :return: the grade object/ None
        """
        return self.__repository.find_by_id(int(str(assID) + str(studID)))

    def add_grade(self, assID, studID, grade, student):
        """
        Adds a grade object to the dictionary
        :param student: student object
        :param assID: assignment id
        :param studID: student id
        :param grade: grade
        :return: nothing
        """
        self.__repository.save(Grade(int(str(assID) + str(studID)), assID, studID, student, grade))
        UndoManager.register_operation(self.__repository, UndoHandler.ADD_GRADE, self.find_grade(assID, studID))

    def delete_grade(self, assID, studID, student):
        """
        Deletes a grade object from the dictionary
        :param student: student object
        :param assID: assignment id
        :param studID: student id
        :return: nothing
        """
        if self.find_grade(assID, studID) is not None:
            UndoManager.register_operation(self.__repository, UndoHandler.DELETE_GRADE, self.find_grade(assID, studID),
                                           "delete_grade")
            self.__repository.delete(Grade(int(str(assID) + str(studID)), assID, studID, student, 0.0))

    def get_assignments_of_student(self, id):
        """
        Returns the list of assignments of a student
        :param id: student id
        :return: list of assignments
        """
        list = self.__repository.get_all()
        a_list = []
        for a in list:
            if a.studID == id:
                a_list.append(a)
        return a_list

    def update_grade(self, assID=None, studID=None, grade=None, student=None):
        """
        Updates the grade of a grade object
        :param student: student object
        :param assID: assignment id
        :param studID: student id
        :param grade: new grade
        :return: nothing
        """
        if type(assID) == Student:
            grades = self.get_all_grades()
            for elem in grades:
                if elem.studID == assID.id:
                    UndoManager.register_operation(self.__repository, UndoHandler.UPDATE_GRADE,
                                                   self.find_grade(elem.assID, elem.studID), "update_grade")
                    self.__repository.update(
                        Grade(int(str(elem.assID) + str(elem.studID)), elem.assID, elem.studID, assID.name,
                              elem.grade))
                else:
                    UndoManager.register_operation(self.__repository, UndoHandler.UPDATE_GRADE,
                                                   self.find_grade(assID, studID), "update_grade")
                    self.__repository.update(Grade(int(str(assID) + str(studID)), assID, studID, student, grade))

    def get_all_grades(self):
        """
        Returns a list of all grade objects
        :return: a list of grade objects
        """
        return self.__repository.get_all()

    def __len__(self):
        return len(self.__repository)


class GradeServiceTest(unittest.TestCase):
    def setUp(self):
        self.grades = GradeService(Repository(GradeValidator))
        self.grades.add_grade(1, 4, 8.4, "Lukas")
        self.grades.add_grade(7, 2, 6.3, "Victor")

    def test_add(self):
        self.assertEqual(len(self.grades), 2)
        self.grades.add_grade(3, 4, 2.2, "Lukas")
        self.assertEqual(len(self.grades), 3)
        try:
            self.grades.add_grade(1, 4, 0.0, "Lukas")
        except RepositoryError:
            pass

        try:
            self.grades.add_grade("5t", 2, 3, "Victor")
        except GradeError:
            pass

        try:
            self.grades.add_grade(2, 2, 11, "Victor")
        except GradeError:
            pass

    def test_delete(self):
        self.grades.delete_grade(1, 4, "Lukas")
        self.assertEqual(len(self.grades), 1)
        try:
            self.grades.delete_grade(2, 5, "Radu")
        except RepositoryError:
            pass

    def test_update(self):
        self.grades.update_grade(1, 4, 10, "Lukas")
        gr = self.grades.get_all_grades()
        self.assertEqual(gr[0].grade, 10)
        try:
            self.grades.update_grade(1, 4, 11, "Lukas")
            self.grades.update_grade("ft", 4, 5, "Lukas")
        except GradeError:
            pass

        try:
            self.grades.update_grade(4, 5, 7, "Radu")
        except RepositoryError:
            pass

    def test_get_assignments_of_student(self):
        list = self.grades.get_assignments_of_student(4)
        gr = self.grades.get_all_grades()
        self.assertEqual(list[0], gr[0])
        list = self.grades.get_assignments_of_student(5)
        self.assertEqual(len(list), 0)

    def test_get(self):
        list = self.grades.get_all_grades()
        self.assertEqual(len(list), 2)
        self.assertEqual(list[0], Grade(1, 4, 8.4, Student(4, "Lukas", 4)))
