class LabError(Exception):
    pass


class ValidatorError(LabError):
    pass


class StudentError(Exception):
    pass


class AssignmentError(Exception):
    pass


class GradeError(Exception):
    pass


class StudentValidator:
    @staticmethod
    def validate(student):
        try:
            student.id = int(student.id)
        except ValueError:
            raise StudentError('invalid id\n')

        if student.id < 0:
            raise StudentError('invalid id\n')

        if type(student.name) != str:
            raise StudentError('invalid name\n')

        elif student.name == '':
            raise StudentError('invalid name\n')

        try:
            student.group = int(student.group)
        except ValueError:
            raise StudentError('invalid group')

        if student.group < 0:
            raise StudentError('invalid group')


class AssignmentValidator:
    @staticmethod
    def validate(assignment):
        try:
            assignment.id = int(assignment.id)
        except ValueError:
            raise AssignmentError('invalid id\n')

        if assignment.id < 0:
            raise AssignmentError('invalid id\n')

        if type(assignment.description) != str:
            raise AssignmentError('invalid description\n')

        elif assignment.description == '':
            raise AssignmentError('invalid description\n')

        from datetime import date
        if type(assignment.deadline) != date:
            raise AssignmentError('invalid deadline')


class GradeValidator:
    @staticmethod
    def validate(grade):
        try:
            grade.assID = int(grade.assID)
        except ValueError:
            raise GradeError('invalid assignment id\n')

        if grade.assID < 0:
            raise GradeError('invalid assignment id\n')

        try:
            grade.studID = int(grade.studID)
        except ValueError:
            raise GradeError('invalid student id\n')

        if grade.studID < 0:
            raise GradeError('invalid student id\n')

        try:
            grade.grade = float(grade.grade)
        except ValueError:
            raise GradeError('invalid grade')

        if grade.grade < 0.0 or grade.grade > 10.0:
            raise GradeError('invalid grade')
