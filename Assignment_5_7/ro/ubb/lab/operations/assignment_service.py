import unittest
from datetime import date

from ro.ubb.lab.domain.entities import Assignment, AssignmentValidator, AssignmentError
from ro.ubb.lab.operations.undo.handlers import UndoHandler
from ro.ubb.lab.operations.undo.manager import UndoManager
from ro.ubb.lab.repository.repository import Repository, RepositoryError


class AssignmentService:
    def __init__(self, repository):
        self.__repository = repository

    def add_assignment(self, id, desc, deadline):
        """
        Adds a new assignment
        :param id: assignment id
        :param desc: assignment description
        :param deadline: assignment deadline
        :return: nothing
        """
        self.__repository.save(Assignment(id, desc, deadline))

        UndoManager.register_operation(self.__repository, UndoHandler.ADD_ASSIGNMENT, self.find_assignment(id))

    def delete_assignment(self, id):
        """
        Deletes an assignment
        :param id: assignment id to delete
        :return: nothing
        """
        UndoManager.register_operation(self.__repository, UndoHandler.DELETE_ASSIGNMENT, self.find_assignment(id),
                                       "delete_assignment")

        self.__repository.delete(Assignment(id, "random", date.today()))

    def update_assignment(self, id, desc, deadline):
        """
        Updates the description and/or deadline of an assignment
        :param id: assignment id
        :param desc: new description
        :param deadline: new deadline
        :return: nothing
        """
        UndoManager.register_operation(self.__repository, UndoHandler.UPDATE_ASSIGNMENT, self.find_assignment(id))
        self.__repository.update(Assignment(id, desc, deadline))

    def find_assignment(self, id):
        """
        Searches for an assignment in the student dictionary
        :param id: assignment id
        :return: the assignment object if it is found, else None
        """
        return self.__repository.find_by_id(id)

    def get_all_assignments(self):
        """
        Returns a list of all assignments
        :return: a list of all assignments
        """
        return self.__repository.get_all()

    def __len__(self):
        return len(self.__repository)


class AssignmentServiceTest(unittest.TestCase):
    def setUp(self):
        self.assignments = AssignmentService(Repository(AssignmentValidator))
        self.assignments.add_assignment(4, "desc", date(2018, 7, 7))
        self.assignments.add_assignment(1, "desc2", date(2018, 6, 6))

    def test_add(self):
        self.assertEqual(len(self.assignments), 2)
        self.assignments.add_assignment(2, "desc3", date(2018, 8, 8))
        self.assertEqual(len(self.assignments), 3)
        try:
            self.assignments.add_assignment("dsc", "desc4", date(2018, 5, 5))
        except AssignmentError:
            pass

    def test_delete(self):
        self.assignments.delete_assignment(4)
        self.assertEqual(len(self.assignments), 1)
        try:
            self.assignments.delete_assignment(5)
        except RepositoryError:
            pass

    def test_update(self):
        self.assignments.update_assignment(4, "new desc", date(2018, 7, 7))
        ass = self.assignments.get_all_assignments()
        self.assertEqual(ass[0].description, "new desc")
        self.assignments.update_assignment(1, "desc2", date(2018, 10, 10))
        ass = self.assignments.get_all_assignments()
        self.assertEqual(ass[0].deadline, date(2018, 7, 7))
        try:
            self.assignments.update_assignment(6, "desc6", date(2018, 9, 9))
        except RepositoryError:
            pass

    def test_get(self):
        ass = self.assignments.get_all_assignments()
        self.assertEqual(len(ass), 2)
        self.assertEqual(ass[0], Assignment(4, "desc", date(2018, 7, 7)))
