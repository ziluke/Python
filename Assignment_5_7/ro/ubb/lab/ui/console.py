import datetime
import random
from datetime import date

from ro.ubb.lab.operations.redo.manager import RedoManager
from ro.ubb.lab.operations.undo.manager import UndoManager
from ro.ubb.lab.repository.Repo_error import RepositoryError



class Console:
    def __init__(self, student_service, assingnment_service, grade_service, report_service, repo):
        self.__student_service = student_service
        self.__assignment_service = assingnment_service
        self.__grade_service = grade_service
        self.__report_service = report_service
        self.__repo = repo
        self.__options = {1: self.__ui_add_student,
                          2: self.__ui_delete_student,
                          3: self.__ui_update_student,
                          4: self.__ui_print_students,
                          5: self.__ui_add_assignment,
                          6: self.__ui_delete_assignment,
                          7: self.__ui_update_assignment,
                          8: self.__ui_print_assignments,
                          9: self.__ui_give_assignment,
                          10: self.__ui_print_grades,
                          11: self.__ui_grade_student,
                          12: self.__ui_statistics,
                          13: self.__undo,
                          14: self.__redo
                          }

    def __ui_populate(self):
        if self.__repo == " inmemory":
            number_of_items = 10
            names = ["Ana", "Maria", "Alexandru", "Mihaela", "Adrian", "Andrei", "Mihai", "Ionut", "Sinziana", "Matei"]
            now = datetime.datetime.now()

            for n in range(1, number_of_items + 1):
                description = "Assignment_" + str(n)
                name = random.choice(names)
                group = random.randrange(1, 10)
                self.__student_service.add_student(n, name, group)
                self.__assignment_service.add_assignment(n + n, description,
                                                         date(now.year, random.choice([1, 3, 5, 6, 7, 10, 12]),
                                                              random.randrange(1, 31)))
                self.__grade_service.add_grade(n + n, n, round(random.uniform(0.0, 10.0), 1), name)

    # def __startup_students(self):
    #     self.__student_service.add_student(1, 'Andrei', 2)
    #     self.__student_service.add_student(2, 'Bogdan', 3)
    #     self.__student_service.add_student(3, 'Cristi', 4)
    #     self.__student_service.add_student(4, 'Daniel', 2)
    #     self.__student_service.add_student(5, 'Mihai', 1)
    #     self.__student_service.add_student(6, 'Raul', 1)
    #     self.__student_service.add_student(7, 'Paul', 2)
    #     self.__student_service.add_student(8, 'Marius', 3)
    #     self.__student_service.add_student(9, 'Adriana', 2)
    #     self.__student_service.add_student(0, 'Alina', 1)
    #
    # def __startup_assignments(self):
    #     self.__assignment_service.add_assignment(1, "Assignment 1", date(2018, 11, 11))
    #     self.__assignment_service.add_assignment(2, "Assignment 2", date(2018, 12, 1))
    #     self.__assignment_service.add_assignment(3, "Assignment 3", date(2018, 11, 20))
    #     self.__assignment_service.add_assignment(4, 'Assignment 4', date(2019, 2, 2))
    #     self.__assignment_service.add_assignment(5, 'Assignment 5', date(2018, 10, 5))
    #     self.__assignment_service.add_assignment(6, 'Assignment 6', date(2018, 11, 10))
    #     self.__assignment_service.add_assignment(7, 'Assignment 7', date(2018, 12, 5))
    #     self.__assignment_service.add_assignment(8, 'Assignment 8', date(2018, 12, 2))
    #     self.__assignment_service.add_assignment(9, 'Assignment 9', date(2018, 9, 4))
    #     self.__assignment_service.add_assignment(10, 'Assignment 10', date(2018, 11, 30))
    #
    # def __startup_grades(self):
    #     self.__grade_service.add_grade(1, 1, 9.0, Student(1, 'Andrei', 2))
    #     self.__grade_service.add_grade(8, 5, 8.0, Student(8, 'Marius', 3))
    #     self.__grade_service.add_grade(7, 4, 7.5, Student(4, 'Daniel', 2))
    #     self.__grade_service.add_grade(2, 1, 0.0, Student(1, 'Andrei', 2))
    #     self.__grade_service.add_grade(5, 2, 3.0, Student(2, 'Bogdan', 3))
    #     self.__grade_service.add_grade(7, 7, 10.0, Student(7, 'Paul', 2))
    #     self.__grade_service.add_grade(9, 2, 0.0, Student(2, 'Bogdan', 3))
    #     self.__grade_service.add_grade(4, 8, 7.2, Student(8, 'Marius', 3))
    #     self.__grade_service.add_grade(6, 9, 7.0, Student(9, 'Adriana', 2))
    #     self.__grade_service.add_grade(10, 1, 10.0, Student(1, 'Alina', 1))

    def __startup(self):
        self.__ui_populate()

    def __ui_add_student(self):
        id = input("ID: ")
        name = input("Name: ")
        group = input("Group: ")
        try:
            id = int(id)
            group = int(group)
            self.__student_service.add_student(id, name, group)
        except RepositoryError as re:
            print("Invalid add: ", re)
        except ValueError:
            print("Invalid input data!")

    def __ui_delete_student(self):
        id = input("ID of the student: ")
        try:
            id = int(id)
            self.__student_service.delete_student(id)
            grades = self.__grade_service.get_all_grades()
            for a in grades:
                if a.studID == int(id):
                    self.__grade_service.delete_grade(a.assID, a.studID, a.grade)
        except RepositoryError as re:
            print("Invalid delete: ", re)
        except ValueError:
            print("Invalid id!")

    def __ui_update_student(self):
        id = input("ID of the student you want to update: ")
        up = input("What do you want to update? Name/Group/Both ")
        up = [s.strip() for s in up.split()]
        try:
            id = int(id)
            if len(up) > 1 or len(up) == 0:
                raise RepositoryError("Update takes just one argument!")
            else:
                update = up[0]
            if update.upper() == "NAME":
                new_name = input("Enter new name: ")
                self.__student_service.update_student(id, new_name)
                self.__grade_service.update_grade(self.__student_service.find_student(id))
            elif update.upper() == "GROUP":
                new_group = int(input("Enter new group: "))
                self.__student_service.update_student(id, new_group)
            elif update.upper() == "BOTH":
                new_name = input("Enter new name: ")
                new_group = int(input("Enter new group: "))
                self.__student_service.update_student(id, new_name, new_group)
                self.__grade_service.update_grade(self.__student_service.find_student(id))
            else:
                print("Invalid choice!")
        except RepositoryError as re:
            print("Invalid update: ", re)
        except ValueError:
            print("Invalid id!")

    def __ui_print_students(self):
        for st in self.__student_service.get_all_students():
            print(st)

    def __ui_add_assignment(self):
        id = input("ID: ")
        desc = input("Description: ")
        year = input("Deadline year: ")
        month = input("Deadline month: ")
        day = input("Deadline day: ")
        try:
            deadline = date(int(year), int(month), int(day))
            self.__assignment_service.add_assignment(id, desc, deadline)
        except RepositoryError as re:
            print("Invalid add: ", re)
        except ValueError:
            print("Invalid date!")

    def __ui_delete_assignment(self):
        id = input("ID of assignment you want to delete: ")
        try:
            id = int(id)
            self.__assignment_service.delete_assignment(id)
            grades = self.__grade_service.get_all_grades()
            for a in grades:
                if a.assID == int(id):
                    self.__grade_service.delete_grade(a.assID, a.studID, a.grade)
        except RepositoryError as re:
            print("Invalid delete: ", re)
        except ValueError:
            print("Invalid id!")

    def __ui_update_assignment(self):
        id = input("ID of assignment you want to update: ")
        up = input("What do you want to update? Description/Deadline/Both ")
        up = [s.strip() for s in up.split()]
        try:
            if len(up) > 1 or len(up) == 0:
                raise RepositoryError("Update takes just one argument!")
            else:
                update = up[0]
            id = int(id)
            assignment = self.__assignment_service.find_assignment(id)
            if update.upper() == "DESCRIPTION":
                new_desc = input("New description: ")
                self.__assignment_service.update_assignment(id, new_desc, assignment.deadline)
            elif update.upper() == "DEADLINE":
                new_y = input("New year: ")
                new_m = input("New month: ")
                new_d = input("New day: ")
                new_deadline = date(int(new_y), int(new_m), int(new_d))
                self.__assignment_service.update_assignment(id, assignment.description, new_deadline)
            elif update.upper() == "BOTH":
                new_desc = input("New description: ")
                new_y = input("New year: ")
                new_m = input("New month: ")
                new_d = input("New day: ")
                new_deadline = date(int(new_y), int(new_m), int(new_d))
                self.__assignment_service.update_assignment(id, new_desc, new_deadline)
            else:
                print("invalid choice!")
        except RepositoryError as re:
            print("Invalid update: ", re)
        except ValueError:
            print("Invalid id/deadline!")

    def __ui_print_assignments(self):
        for st in self.__assignment_service.get_all_assignments():
            print(st)

    @staticmethod
    def __print(elem):
        for i in elem:
            print(i)

    def __ui_give_assignment(self):
        """Bug: give an assignment to a student that already has it, but when you give it to a new student, BUG!"""
        self.__print(self.__assignment_service.get_all_assignments())
        try:
            assID = input("Choose an assignment id: ")
            opt = input("Whom do you want to assign this assignment? Group/Student ")
            opt = [s.strip() for s in opt.split()]
            if len(opt) > 1:
                raise RepositoryError("Too many arguments!")
            option = opt[0]
            valid = True
            while valid:
                if option.upper() == "STUDENT":
                    studID = int(input("Enter student ID: "))
                    x = ''
                    while x.upper() != "X":
                        if self.__student_service.find_student(studID):
                            try:
                                if not self.__grade_service.find_grade(assID, studID):
                                    self.__grade_service.add_grade(int(str(assID) + str(studID)), assID, studID, 0,
                                                                   self.__student_service.find_student(studID).name)
                                else:
                                    print("This student already has this assignment")
                            except RepositoryError as re:
                                print(re)
                        else:
                            print("This student does not exist")
                        x = input("To exit, press X. Else, enter another student ID: ")
                        studID = int(x)
                    valid = False
                elif option.upper() == "GROUP":
                    gr = int(input("To which group do you want to assign this assignment? "))
                    all_students = self.__student_service.get_all_students()
                    for st in all_students:
                        if st.group == gr:
                            self.__grade_service.add_grade(int(str(assID) + str(st.id)), assID, st.id, 0, st.name)
                    valid = False
        except RepositoryError as re:
            print("Error: ", re)
        except ValueError:
            print("Invalid id!")

    def __ui_print_grades(self):
        for st in self.__grade_service.get_all_grades():
            print(st)

    def __ui_grade_student(self):
        id = input("Enter the ID of the student: ")
        try:
            id = int(id)
            if self.__student_service.find_student(id):
                a_list = self.__grade_service.get_assignments_of_student(id)
                self.__print(a_list)
                assID = int(input("Assignment ID: "))
                if self.__assignment_service.find_assignment(assID):
                    ct = 0
                    for a in a_list:
                        if a.assID == assID and a.grade == 0.0:
                            ct += 1
                            grade = float(input("Enter grade: "))
                            self.__grade_service.update_grade(assID, id, grade, self.__student_service.find_student(id))
                    if ct == 0:
                        print("Assignments already graded!")
                else:
                    raise RepositoryError("Object with that id does not exist!")
            else:
                raise RepositoryError("Object with that id does not exist!")
        except RepositoryError as re:
            print("Error: ", re)
        except ValueError:
            print("Invalid id!")

    def __ui_students_with_ass(self):
        try:
            id = int(input("Enter assignment id: "))
            sorted_l = self.__report_service.filter_dtos(id)
            self.__print(sorted_l)
        except ValueError:
            print("Invalid assignment id!")

    def __ui_late_ass(self):
        today = date.today()
        self.__print(self.__report_service.filter_late(today))

    def __ui_best_situation(self):
        self.__print(self.__report_service.filter_best_situations())

    def __ui_ass_with_grade(self):
        self.__print(self.__report_service.filter_best_assignment())

    def __ui_statistics(self):
        options = {1: self.__ui_students_with_ass,
                   2: self.__ui_late_ass,
                   3: self.__ui_best_situation,
                   4: self.__ui_ass_with_grade}

        print("\n1. All students who received a given assignment\n"
              "2. All student who are late in handing in an assignment\n"
              "3. Students with the best school situation\n"
              "4. All graded assignments\n")
        try:
            opt = int(input("Option: "))
            options[opt]()
        except ValueError:
            print("Invalid option!")

    def __undo(self):
        UndoManager.undo()

    def __redo(self):
        RedoManager.redo()

    def run_menu(self):
        self.__startup()
        while True:
            self.__print_menu()
            opt = input("Option: ")
            if opt == "x":
                break
            try:
                opt = int(opt)
                self.__options[opt]()
            except ValueError:
                print("Invalid option!")
            except KeyError:
                print("Option not implemented!")

    @staticmethod
    def __print_menu():
        print("\n1. Add student\n"
              "2. Delete student\n"
              "3. Update student\n"
              "4. Print students\n"
              "5. Add assignment\n"
              "6. Delete assignment\n"
              "7. Update assignment\n"
              "8. Print assignments\n"
              "9. Give assignments\n"
              "10. See all grades\n"
              "11. Grade assignments\n"
              "12. Statistics\n"
              "13. Undo\n"
              "14. Redo\n"
              "x. Exit")
