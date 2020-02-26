from enum import Enum


def add_student_redo_handler(student_repo, student):
    student_repo.save(student)


def delete_student_redo_handler(student_repo, student):
    student_repo.delete(student)


def update_student_redo_handler(student_repo, student):
    student_repo.update(student)


def add_assignment_redo_handler(assignment_repo, assignment):
    assignment_repo.save(assignment)


def delete_assignment_redo_handler(assignment_repo, assignment):
    assignment_repo.delete(assignment)


def update_assignment_redo_handler(assignment_repo, assignment):
    assignment_repo.update(assignment)


def add_grade_redo_handler(grade_repo, grade):
    grade_repo.save(grade)


def delete_grade_redo_handler(grade_repo, grade):
    grade_repo.delete(grade)


def update_grade_redo_handler(grade_repo, grade):
    grade_repo.update(grade)


class RedoHandler(Enum):
    ADD_STUDENT = add_student_redo_handler
    DELETE_STUDENT = delete_student_redo_handler
    UPDATE_STUDENT = update_student_redo_handler
    ADD_ASSIGNMENT = add_assignment_redo_handler
    DELETE_ASSIGNMENT = delete_assignment_redo_handler
    UPDATE_ASSIGNMENT = update_assignment_redo_handler
    ADD_GRADE = add_grade_redo_handler
    DELETE_GRADE = delete_grade_redo_handler
    UPDATE_GRADE = update_grade_redo_handler
