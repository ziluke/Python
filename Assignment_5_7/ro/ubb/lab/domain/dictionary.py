class My_Dict(dict):
    def __init__(self):
        super(My_Dict, self).__init__()

    def __setitem__(self, key, value):
        super(My_Dict, self).__setitem__(key, value)

    def __delitem__(self, key):
        super(My_Dict, self).__delitem__(key)

    def __iter__(self):
        super(My_Dict, self).__iter__()

    @staticmethod
    def sort(list, function):
        """
        GNOME SORT
        :param list: list to be sorted
        :param function: criteria by which to sort the list
        :return: the sorted list
        """
        index = 0
        n = len(list)

        if n == 1:
            return list

        while index < n:
            if index == 0:
                index = index + 1
            if function(list[index], list[index - 1]):
                index = index + 1
            else:
                list[index], list[index - 1] = list[index - 1], list[index]
                index = index - 1
        return list
