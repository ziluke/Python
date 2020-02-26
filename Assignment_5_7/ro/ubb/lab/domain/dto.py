import unittest
from datetime import date

from ro.ubb.lab.domain.entities import Student, Assignment, Grade


class Dto(object):
    """
    Data Transfer Object Class
    """

    def __init__(self, stud_name, assID, grade):
        """
        Creates a dto
        :param stud_name: student name
        :param assID: assignment id
        :param grade: grade
        """
        self.__name = stud_name
        self.__assID = assID
        self.__grade = grade

    @property
    def name(self):
        """
        getter property for the name
        :return: name of the student
        """
        return self.__name

    @name.setter
    def name(self, name):
        """
        setter property for the name
        :param name: name to assign
        :return: nothing
        """
        self.__name = name

    @property
    def assID(self):
        """
        getter property for the assignment id
        :return: assignment id
        """
        return self.__assID

    @assID.setter
    def assID(self, id):
        """
        setter property for the assignment id
        :param id: assignment id to assign
        :return: nothing
        """
        self.__assID = id

    @property
    def grade(self):
        """
        getter property for the grade
        :return: grade
        """
        return self.__grade

    @grade.setter
    def grade(self, grade):
        """
        setter property for the grade
        :param grade: grade to assign
        :return: nothing
        """
        self.__grade = grade

    def __str__(self):
        """
        Function that prints a dto
        :return: string of the printing format of a dto
        """
        return "Student Name: {0} Assignment: {1} Grade: {2}".format(self.__name, self.__assID, self.__grade)


class Assembler:
    """
    DTO Creater
    """

    @staticmethod
    def create_dto(student, assignment, grades):
        """
        Creates a dto object
        :param student: student object
        :param assignment: assignment object
        :param grades: grade object
        :return: dto
        """
        return Dto(student.name, assignment.id, grades.grade)
