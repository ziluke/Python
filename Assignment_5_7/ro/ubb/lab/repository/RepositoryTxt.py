from ro.ubb.lab.domain.dictionary import My_Dict
from ro.ubb.lab.repository.Repo_error import RepositoryError


class RepositoryTxt:
    def __init__(self, f_name, validator_class, entity_class):
        self.__validator = validator_class
        self.__f_name = f_name
        self.__entity_class = entity_class

    def find_by_id(self, id):
        objects = self.__get_all()
        if id not in objects:
            return None
        return objects[id]

    def save(self, object):
        self.__validator.validate(object)
        try:
            file = open(self.__f_name, "a")
        except EOFError:
            raise RepositoryError("File is empty!")
        if self.find_by_id(object.id) is not None:
            raise RepositoryError("Id already taken!")
        file.write(str(object) + "\n")
        file.close()

    def delete(self, object):
        self.__validator.validate(object)
        if self.find_by_id(object.id) is not None:
            objects = self.__get_all()
            del objects[object.id]
        else:
            raise RepositoryError("This entity does not exist")
        self.overwrite(objects)

    def update(self, new_object):
        self.__validator.validate(new_object)
        if self.find_by_id(new_object.id) is None:
            raise RepositoryError("Object doesn't exist!")
        objects = self.__get_all()
        objects[new_object.id] = new_object
        self.overwrite(objects)

    def overwrite(self, objects):
        file = open(self.__f_name, "w")
        for el in objects.values():
            file.write(str(el) + "\n")
        file.close()

    def get_all(self):
        return list(self.__get_all().values())

    def __get_all(self):
        objects = My_Dict()
        try:
            file = open(self.__f_name, "r")
            line = file.readline().split()
            while len(line) > 0:
                object = []
                for i in range(0, len(line)):
                    if "." in line[i]:
                        object.append(float(line[i]))
                    elif line[i].isnumeric():
                        object.append(int(line[i]))
                    elif line[i] in ["Name:", "ID:", "Description:", "Student", "Id:", "Group:", "Grade:", "Assignment",
                                     "Deadline:"]:
                        i += 1
                    else:
                        object.append(line[i])
                new_object = self.__entity_class(*object)
                objects[new_object.id] = new_object
                line = file.readline().split()
            file.close()
        except EOFError:
            raise RepositoryError("File is empty!")
        except IOError:
            raise RepositoryError("Invalid file!")

        return objects
