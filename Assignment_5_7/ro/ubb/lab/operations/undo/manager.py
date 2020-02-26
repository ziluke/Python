from dataclasses import dataclass

from ro.ubb.lab.operations.undo.handlers import UndoHandler


@dataclass
class UndoOperation:
    __source_object: object
    __handler: UndoHandler
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


class UndoManager:
    _undo_operations = []
    _cascading = []
    _index = 0
    _i = 0
    _j = 0
    _casc_i = -1

    @staticmethod
    def register_operation(source_object, handler, args, cascade=None):
        if cascade != "delete_student" and cascade != "delete_assignment" and cascade != "delete_grade" and cascade != "update_student" and cascade != "update_grade":
            UndoManager._undo_operations.append(
                UndoOperation(source_object, handler, args))
            UndoManager._index += 1
        else:
            if cascade == "delete_student" or cascade == "delete_assignment" or cascade == "update_student":
                UndoManager._undo_operations.append(
                    UndoOperation(source_object, handler, args))
                UndoManager._index += 1
                UndoManager._i = UndoManager._index
            else:
                UndoManager._undo_operations.append(
                    UndoOperation(source_object, handler, args))
                UndoManager._index += 1
                UndoManager._j = UndoManager._index
        if (UndoManager._i,
            UndoManager._j) not in UndoManager._cascading and UndoManager._j != 0 and UndoManager._i != 0:
            UndoManager._cascading.append((UndoManager._i, UndoManager._j))
            UndoManager._casc_i += 1

    @staticmethod
    def undo():
        try:
            if not UndoManager._cascading:
                undo_operation = UndoManager._undo_operations.pop()
                undo_operation.handler(undo_operation.source_object,
                                       undo_operation.args)
                UndoManager._index -= 1
            elif UndoManager._cascading[UndoManager._casc_i][1] != UndoManager._index:
                undo_operation = UndoManager._undo_operations.pop()
                undo_operation.handler(undo_operation.source_object,
                                       undo_operation.args)
                UndoManager._index -= 1
            else:
                while UndoManager._cascading[UndoManager._casc_i][0] <= UndoManager._index:
                    undo_operation = UndoManager._undo_operations.pop()
                    undo_operation.handler(undo_operation.source_object,
                                           undo_operation.args)
                    UndoManager._index -= 1
        except IndexError:
            print("Nothing to undo!")
