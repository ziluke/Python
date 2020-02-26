import traceback

from ro.ubb.lab.domain.entities import Student, Assignment, Grade
from ro.ubb.lab.operations.assignment_service import AssignmentService
from ro.ubb.lab.domain.validators import AssignmentValidator, StudentValidator, GradeValidator
from ro.ubb.lab.operations.grade_service import GradeService
from ro.ubb.lab.operations.report_service import ReportService
from ro.ubb.lab.repository.RepositoryPickle import RepositoryPickle
from ro.ubb.lab.repository.RepositoryTxt import RepositoryTxt
from ro.ubb.lab.repository.repository import Repository
from ro.ubb.lab.operations.student_service import StudentService
from ro.ubb.lab.ui.console import Console


def read_file():
    settings = open("settings.properties.txt", "r")
    line = settings.readline().strip()
    repo = line.split("=")[1]
    line = settings.readline().strip()
    input = []
    while line != "":
        aux = line.split("=")
        input.append(aux[1])
        line = settings.readline().strip()
    settings.close()
    return repo, input


if __name__ == '__main__':
    try:
        repo, input = read_file()
        if repo == " inmemory":
            student_repository = Repository(StudentValidator)
            assignment_repository = Repository(AssignmentValidator)
            grade_repository = Repository(GradeValidator)
            report_service = ReportService(student_repository, assignment_repository, grade_repository)

        elif repo == " text":
            student_repository = RepositoryTxt(input[0], StudentValidator, Student)
            assignment_repository = RepositoryTxt(input[1], AssignmentValidator, Assignment)
            grade_repository = RepositoryTxt(input[2], GradeValidator, Grade)

        elif repo == " pickle":
            student_repository = RepositoryPickle(input[0], StudentValidator, Student)
            assignment_repository = RepositoryPickle(input[1], AssignmentValidator, Assignment)
            grade_repository = RepositoryPickle(input[2], GradeValidator, Grade)

        student_service = StudentService(student_repository)
        assignment_service = AssignmentService(assignment_repository)
        grade_service = GradeService(grade_repository)
        report_service = ReportService(student_repository, assignment_repository, grade_repository)

        console = Console(student_service, assignment_service, grade_service, report_service, repo)
        console.run_menu()
    except Exception as ex:
        print("Exception: ", ex, "\nPrinting traceback")
        traceback.print_exc()
