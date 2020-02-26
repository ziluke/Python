from datetime import date

from ro.ubb.lab.domain.dictionary import My_Dict
from ro.ubb.lab.domain.dto import Dto, Assembler
from ro.ubb.lab.domain.entities import Grade, Assignment


class ReportService:
    def __init__(self, student_repository, assignment_repository, grade_repository):
        self.__student_repository = student_repository
        self.__assignment_repository = assignment_repository
        self.__grade_repository = grade_repository

    def __get_dtos(self, id):
        """
        Creates and returns a list of all students that have a given assignment
        :param id: assignment id
        :return: list of DTOs
        """
        dtos = My_Dict()
        index = 0
        for grade in self.__grade_repository.get_all():
            student = self.__student_repository.find_by_id(grade.studID)
            if grade.assID == id:
                assignment = self.__assignment_repository.find_by_id(id)
                dto = Assembler.create_dto(student, assignment, grade)
                dtos[index] = dto
                index += 1
        return dtos

    def filter_dtos(self, id):
        """
        Sorts the list in ascending order by name and then assignment id
        :param id: assignment id
        :return: the sorted list
        """
        dtos = self.__get_dtos(id)
        return dtos.sort(list(dtos.values()), self.asc_name)

    @staticmethod
    def asc_name(obj1, obj2):
        if obj1.name > obj2.name:
            return obj1
        elif obj2.name > obj1.name:
            return obj2
        else:
            return obj1.assID > obj2.assID

    def filter_late(self, today):
        """
        Creates and returns a list of all students who are late in handing in an assignment
        :param today: today's date
        :return: a list of DTOs
        """
        dtos = My_Dict()
        index = 0

        for grade in self.__grade_repository.get_all():
            student = self.__student_repository.find_by_id(grade.studID)
            assignment = self.__assignment_repository.find_by_id(grade.assID)
            if today > assignment.deadline and grade.grade == 0.0:
                dto = Assembler.create_dto(student, assignment, grade)
                dtos[index] = dto
                index += 1
        return dtos

    def __best_situation(self):
        """
        Creates and returns a list of all students together with all their assignments and their mean
        :return: list of DTOs
        """
        dtos = My_Dict()
        index = 0
        for student in self.__student_repository.get_all():
            mean = 0
            ct = 0
            assignments = []
            for grade in self.__grade_repository.get_all():
                if student.id == grade.studID:
                    assignments.append(grade.assID)
                    mean = mean + grade.grade
                    ct += 1
            if ct != 0:
                mean = mean / ct
            for i in range(len(assignments)):
                grade = Grade(int(str(assignments[i]) + str(student.id)), assignments[i], student.id, student.name,
                              mean)
                dto = Assembler.create_dto(student, Assignment(assignments[i], "random", date.today()), grade)
                dtos[index] = dto
                index += 1
        return dtos

    def filter_best_situations(self):
        """
        Sorts a list of DTOs according to their mean in descending order
        :return: the sorted list
        """
        dtos = self.__best_situation()
        return dtos.sort(list(dtos.values()), self.desc_mean)

    @staticmethod
    def desc_mean(obj1, obj2):
        return obj1.grade < obj2.grade

    def __best_assignment(self):
        """
        Creates and returns a list of all assignments that have at least one grade
        :return: a list of DTOs
        """
        dtos = My_Dict()
        index = 0
        for assignment in self.__assignment_repository.get_all():
            mean = 0
            ct = 0
            students = []
            for grade in self.__grade_repository.get_all():
                if assignment.id == grade.assID:
                    stud_name = self.__student_repository.find_by_id(grade.studID)
                    students.append(stud_name.name)
                    mean = mean + grade.grade
                    ct += 1
            if mean != 0:
                mean = mean / ct
                dto = Dto(students, assignment.id, mean)
                dtos[index] = dto
                index += 1
        return dtos

    def filter_best_assignment(self):
        """
        Sorts a list according to their mean in descending order
        :return: the sorted list
        """
        dtos = self.__best_assignment()
        return dtos.sort(list(dtos.values()), self.desc_mean)
