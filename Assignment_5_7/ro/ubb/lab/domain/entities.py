import unittest
from datetime import date

from ro.ubb.lab.domain.validators import *


class Student(object):
    """
    Student class
    """

    def __init__(self, id, name, group):
        """
        Creates an object of type student
        :param id: student id
        :param name: student name
        :param group: student group
        """
        self.__id = id

        name = [s.strip() for s in name.split()]

        nm = name[0]
        for n in name[1:]:
            nm = nm + " " + n

        self.__name = nm

        self.__group = group

    def __str__(self):
        """
        Function that prints a student
        :return: a sting that shows the students id, name and group
        """
        return "ID: {0} Name: {1} Group: {2}".format(self.__id, self.__name.upper(), self.__group)

    @property
    def id(self):
        """
        getter property for the id
        :return: student id
        """
        return self.__id

    @property
    def name(self):
        """
        getter property for the name
        :return: student name
        """
        return self.__name

    @property
    def group(self):
        """
        getter property for the group
        :return: student group
        """
        return self.__group

    @group.setter
    def group(self, group):
        """
        setter property for the group
        :param group: the group that should be assigned
        :return: nothing
        """
        self.__group = group

    @id.setter
    def id(self, id):
        """
        setter property for the id
        :param id: the id that should be assigned
        :return: nothing
        """
        self.__id = id

    @name.setter
    def name(self, name):
        """
        setter property for the name
        :param name: the name that should be assigned
        :return: nothing
        """
        self.__name = name

    def __eq__(self, st):
        """
        Function that evaluates if two students are the same
        :param st: student object to compare to
        :return: True/False
        """
        if self.__id == st.__id:
            return True
        return False


class Assignment(object):
    """
    Assignment Class
    """

    def __init__(self, id, desc, deadline):
        """
        Initializes an assignment object
        :param id: assignment id
        :param desc: assignment description
        :param deadline: assignment deadline
        """
        self.__id = id

        desc = [s.strip() for s in desc.split()]

        ds = desc[0]
        for d in desc[1:]:
            ds = ds + " " + d

        self.__desc = ds

        self.__deadline = deadline

    def __str__(self):
        """
        Function that prints an assignment
        :return: a sting that shows the assignments id, description and deadline
        """
        return "ID: {0} Description: {1} Deadline: {2}".format(self.__id, self.__desc, self.__deadline)

    @property
    def id(self):
        """
        getter property for the id
        :return: assignment id
        """
        return self.__id

    @property
    def description(self):
        """
        getter property for the description
        :return: assignment description
        """
        return self.__desc

    @property
    def deadline(self):
        """
        getter property for the deadline
        :return: assignment deadline
        """
        return self.__deadline

    @id.setter
    def id(self, id):
        """
        setter property for the assignment id
        :param id: the id to assign
        :return: nothing
        """
        self.__id = id

    @description.setter
    def description(self, desc):
        """
        setter property for the description
        :param desc: the description to assign
        :return: nothing
        """
        self.__desc = desc

    @deadline.setter
    def deadline(self, deadline):
        """
        setter property for the deadline
        :param deadline: the deadline to assign
        :return: nothing
        """
        self.__deadline = deadline

    def __eq__(self, ass):
        """
        Function that evaluates if two assignments are the same
        :param ass: assignment object to compare to
        :return: True/False
        """
        if self.__id == ass.__id:
            return True
        return False


class Grade(object):
    """
    Grade Class
    """

    def __init__(self, id, assID, studID, student, grade):
        """
        Initializes a grade object
        :param assID: assignment id
        :param studID: student id
        :param grade: grade for that assignment
        """
        self.__id = id
        self.__assID = assID
        self.__studID = studID
        self.__grade = grade
        self.__student = student

    def __str__(self):
        """
        Format of how a grade object should be printed
        :return: a string of the grade object representation
        """
        return "ID: {0} Assignment ID: {1} Student ID: {2} Student Name: {3} Grade: {4}".format(self.__id, self.__assID,
                                                                                                self.__studID,
                                                                                                self.__student,
                                                                                                self.__grade)

    @property
    def id(self):
        """
        getter property for the id
        :return: grade id
        """
        return self.__id

    @property
    def student(self):
        return self.__student

    @student.setter
    def student(self, student):
        self.__student = student

    @property
    def assID(self):
        """
        getter property for the assignment id
        :return: assignment id
        """
        return self.__assID

    @property
    def studID(self):
        """
        getter property for the student id
        :return: student id
        """
        return self.__studID

    @property
    def grade(self):
        """
        getter property for the grade
        :return: grade
        """
        return self.__grade

    @id.setter
    def id(self, id):
        """
        setter property for the id
        :param id: the id that should be assigned
        :return: nothing
        """
        self.__id = id

    @assID.setter
    def assID(self, assID):
        """
        setter property for the assignment id
        :param assID: assignment id
        :return: nothing
        """
        self.__assID = assID

    @studID.setter
    def studID(self, studID):
        """
        setter property for the student id
        :param studID: student id
        :return: nothing
        """
        self.__studID = studID

    @grade.setter
    def grade(self, grade):
        """
        setter property for the grade
        :param grade: grade to assign
        :return: nothing
        """
        self.__grade = grade

    def __eq__(self, grade):
        """
        Function that evaluates if two grades are the same
        :param grade: grade object to compare to
        :return: True/False
        """
        if self.__id == grade.__id:
            return True
        return False


class TestStudent(unittest.TestCase):
    def setUp(self):
        self.validator = StudentValidator()
        self.stud1 = Student(13, "Lukas", 2)
        self.stud2 = Student(2, "Victor", 4)
        self.stud3 = Student(3, "Anna", 3)

    def test_validate(self):
        self.assertTrue(self.validator.validate, self.stud1)
        self.assertTrue(self.validator.validate, self.stud2)
        self.stud3.id = "d"
        self.assertRaises(StudentError, self.validator.validate, self.stud3)
        self.stud2.name = 4
        self.assertRaises(StudentError, self.validator.validate, self.stud2)
        self.stud1.group = -5
        self.assertRaises(StudentError, self.validator.validate, self.stud1)

    def test_id(self):
        self.stud1.id = 1
        self.assertEqual(self.stud1.id, 1)
        self.assertTrue(self.validator.validate, self.stud1)
        self.stud1.id = ""
        self.assertRaises(StudentError, self.validator.validate, self.stud1)
        self.stud1.id = "d"
        self.assertRaises(StudentError, self.validator.validate, self.stud1)
        self.stud1.id = -6
        self.assertRaises(StudentError, self.validator.validate, self.stud1)

    def test_name(self):
        self.stud1.name = "Isabella"
        self.assertEqual(self.stud1.name, "Isabella")
        self.assertTrue(self.validator.validate, self.stud1)
        self.stud1.name = ""
        self.assertRaises(StudentError, self.validator.validate, self.stud1)
        self.stud1.name = 6
        self.assertRaises(StudentError, self.validator.validate, self.stud1)

    def test_group(self):
        self.stud1.group = 14
        self.assertEqual(self.stud1.group, 14)
        self.assertTrue(self.validator.validate, self.stud1)
        self.stud1.group = ""
        self.assertRaises(StudentError, self.validator.validate, self.stud1)
        self.stud1.group = "d"
        self.assertRaises(StudentError, self.validator.validate, self.stud1)
        self.stud1.group = -6
        self.assertRaises(StudentError, self.validator.validate, self.stud1)


class TestAssignment(unittest.TestCase):
    def setUp(self):
        self.validator = AssignmentValidator()
        self.ass1 = Assignment(7, "asd", date(2018, 5, 13))
        self.ass2 = Assignment(3, "jkl", date.today())
        self.ass3 = Assignment(14, "qwe", date(2017, 3, 7))

    def test_validate(self):
        self.assertTrue(self.validator.validate, self.ass1)
        self.assertTrue(self.validator.validate, self.ass2)
        self.ass3.id = "d"
        self.assertRaises(AssignmentError, self.validator.validate, self.ass3)
        self.ass2.description = 4
        self.assertRaises(AssignmentError, self.validator.validate, self.ass2)
        self.ass1.deadline = -5
        self.assertRaises(AssignmentError, self.validator.validate, self.ass1)

    def test_id(self):
        self.ass1.id = 1
        self.assertEqual(self.ass1.id, 1)
        self.assertTrue(self.validator.validate, self.ass1)
        self.ass1.id = ""
        self.assertRaises(AssignmentError, self.validator.validate, self.ass1)
        self.ass1.id = "d"
        self.assertRaises(AssignmentError, self.validator.validate, self.ass1)
        self.ass1.id = -6
        self.assertRaises(AssignmentError, self.validator.validate, self.ass1)

    def test_description(self):
        self.ass1.description = "assignment 1"
        self.assertEqual(self.ass1.description, "assignment 1")
        self.assertTrue(self.validator.validate, self.ass1)
        self.ass1.description = ""
        self.assertRaises(AssignmentError, self.validator.validate, self.ass1)
        self.ass1.description = 6
        self.assertRaises(AssignmentError, self.validator.validate, self.ass1)

    def test_deadline(self):
        self.ass1.deadline = date(2018, 6, 6)
        self.assertEqual(self.ass1.deadline, date(2018, 6, 6))
        self.assertTrue(self.validator.validate, self.ass1)
        self.ass1.deadline = ""
        self.assertRaises(AssignmentError, self.validator.validate, self.ass1)
        self.ass1.deadline = 2018 - 6 - 6
        self.assertRaises(AssignmentError, self.validator.validate, self.ass1)


class TestGrade(unittest.TestCase):
    def setUp(self):
        self.validator = GradeValidator()
        self.gr1 = Grade(1232, 12, 32, "Lukas", 10)
        self.gr2 = Grade(11, 1, 1, "Victor", 5)
        self.gr3 = Grade(42, 4, 2, "Mihai", 7)

    def test_validate(self):
        self.assertTrue(self.validator.validate, self.gr1)
        self.assertTrue(self.validator.validate, self.gr2)
        self.gr3.assID = "das"
        self.assertRaises(GradeError, self.validator.validate, self.gr3)
        self.gr3.assID = -4
        self.assertRaises(GradeError, self.validator.validate, self.gr3)
        self.gr2.studID = "das"
        self.assertRaises(GradeError, self.validator.validate, self.gr2)
        self.gr2.studID = -4
        self.assertRaises(GradeError, self.validator.validate, self.gr2)
        self.gr1.grade = "das"
        self.assertRaises(GradeError, self.validator.validate, self.gr1)
        self.gr1.grade = -4
        self.assertRaises(GradeError, self.validator.validate, self.gr1)
        self.gr1.grade = 11
        self.assertRaises(GradeError, self.validator.validate, self.gr1)

    def test_ids(self):
        self.assertEqual(self.gr1.id, 1232)

        self.gr1.assID = 1
        self.assertEqual(self.gr1.assID, 1)
        self.assertTrue(self.validator.validate, self.gr1)
        self.gr1.assID = ""
        self.assertRaises(GradeError, self.validator.validate, self.gr1)
        self.gr1.assID = "d"
        self.assertRaises(GradeError, self.validator.validate, self.gr1)
        self.gr1.assID = -6
        self.assertRaises(GradeError, self.validator.validate, self.gr1)

        self.gr1.studID = 1
        self.assertEqual(self.gr1.studID, 1)
        self.assertTrue(self.validator.validate, self.gr1)
        self.gr1.studID = ""
        self.assertRaises(GradeError, self.validator.validate, self.gr1)
        self.gr1.studID = "d"
        self.assertRaises(GradeError, self.validator.validate, self.gr1)
        self.gr1.studID = -6
        self.assertRaises(GradeError, self.validator.validate, self.gr1)

    def test_grade(self):
        self.gr2.grade = 7.2
        self.assertEqual(self.gr2.grade, 7.2)
        self.assertTrue(self.validator.validate, self.gr2)
        self.gr2.grade = ""
        self.assertRaises(GradeError, self.validator.validate, self.gr2)
        self.gr2.grade = -4
        self.assertRaises(GradeError, self.validator.validate, self.gr2)
        self.gr2.grade = 1123123
        self.assertRaises(GradeError, self.validator.validate, self.gr2)

    def test_student(self):
        self.gr2.student = Student(4, "Alexandra", 5)
        self.assertEqual(self.gr2.student, Student(4, "Alexandra", 5))
