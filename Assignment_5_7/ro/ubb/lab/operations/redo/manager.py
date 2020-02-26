from dataclasses import dataclass

from ro.ubb.lab.operations.redo.handlers import RedoHandler


@dataclass
class RedoOperation:
    __source_object: object
    __handler: RedoHandler
    __args: tuple

    @property
    def source_object(self):
        return self.__source_object

    @property
    def handler(self):
        return self.__handler

    @property
    def args(self):
        return self.__args


class RedoManager:
    __redo_operations = []
    __cascading = []
    __index = 0
    __i = 0
    __j = 0
    __casc_i = -1

    @staticmethod
    def register_operation(source_object, handler, args, cascade=None):
        if cascade != "delete_student" and cascade != "delete_assignment" and cascade != "delete_grade" and cascade != "update_student" and cascade != "update_grade":
            RedoManager.__redo_operations.append(
                RedoOperation(source_object, handler, args))
            RedoManager.__index += 1
        else:
            if cascade == "delete_student" or cascade == "delete_assignment" or cascade == "update_student":
                RedoManager.__redo_operations.append(
                    RedoOperation(source_object, handler, args))
                RedoManager.__index += 1
                RedoManager.__i = RedoManager.__index
            else:
                RedoManager.__redo_operations.append(
                    RedoOperation(source_object, handler, args))
                RedoManager.__index += 1
                RedoManager.__j = RedoManager.__index
        if (RedoManager.__i,
                RedoManager.__j) not in RedoManager.__cascading and RedoManager.__j != 0 and RedoManager.__i != 0:
            RedoManager.__cascading.append((RedoManager.__i, RedoManager.__j))
            RedoManager.__casc_i += 1

    @staticmethod
    def redo():
        try:
            if not RedoManager.__cascading:
                undo_operation = RedoManager.__redo_operations.pop()
                undo_operation.handler(undo_operation.source_object,
                                       undo_operation.args)
                RedoManager.__index -= 1
            elif RedoManager.__cascading[RedoManager.__casc_i][0] != RedoManager.__index:
                redo_operation = RedoManager.__redo_operations.pop()
                redo_operation.handler(redo_operation.source_object,
                                       redo_operation.args)
                RedoManager.__index -= 1
            else:
                while RedoManager.__cascading[RedoManager.__casc_i][1] <= RedoManager.__index:
                    undo_operation = RedoManager.__redo_operations.pop()
                    undo_operation.handler(undo_operation.source_object,
                                           undo_operation.args)
                    RedoManager.__index -= 1
        except IndexError:
            print("Nothing to redo!")
