from enum import Enum

from ro.ubb.lab.operations.redo.handlers import RedoHandler
from ro.ubb.lab.operations.redo.manager import RedoManager


def add_student_undo_handler(student_repo, student):
    RedoManager.register_operation(student_repo, RedoHandler.ADD_STUDENT, student)
    student_repo.delete(student)


def delete_student_undo_handler(student_repo, student):
    RedoManager.register_operation(student_repo, RedoHandler.DELETE_STUDENT, student, "delete_student")
    student_repo.save(student)


def update_student_undo_handler(student_repo, student):
    RedoManager.register_operation(student_repo, RedoHandler.UPDATE_STUDENT, student, "update_student")
    student_repo.update(student)


def add_assignment_undo_handler(assignment_repo, assignment):
    RedoManager.register_operation(assignment_repo, RedoHandler.ADD_ASSIGNMENT, assignment)
    assignment_repo.delete(assignment)


def delete_assignment_undo_handler(assignment_repo, assignment):
    assignment_repo.save(assignment)
    RedoManager.register_operation(assignment_repo, RedoHandler.DELETE_ASSIGNMENT, assignment, "delete_assignment")


def update_assignment_undo_handler(assignment_repo, assignment):
    assignment_repo.update(assignment)
    RedoManager.register_operation(assignment_repo, RedoHandler.UPDATE_ASSIGNMENT, assignment)


def add_grade_undo_handler(grade_repo, grade):
    RedoManager.register_operation(grade_repo, RedoHandler.ADD_GRADE, grade)
    grade_repo.delete(grade)


def delete_grade_undo_handler(grade_repo, grade):
    grade_repo.save(grade)
    RedoManager.register_operation(grade_repo, RedoHandler.DELETE_GRADE, grade, "delete_grade")


def update_grade_undo_handler(grade_repo, grade):
    grade_repo.update(grade)
    RedoManager.register_operation(grade_repo, RedoHandler.UPDATE_GRADE, grade, "update_grade")


class UndoHandler(Enum):
    ADD_STUDENT = add_student_undo_handler
    DELETE_STUDENT = delete_student_undo_handler
    UPDATE_STUDENT = update_student_undo_handler
    ADD_ASSIGNMENT = add_assignment_undo_handler
    DELETE_ASSIGNMENT = delete_assignment_undo_handler
    UPDATE_ASSIGNMENT = update_assignment_undo_handler
    ADD_GRADE = add_grade_undo_handler
    DELETE_GRADE = delete_grade_undo_handler
    UPDATE_GRADE = update_grade_undo_handler
