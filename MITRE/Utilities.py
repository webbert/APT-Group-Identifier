class Utilities:
    def __init__(self, func, iterator):
        func_dict = {"iter_to_str": self.iterator_to_string,
                     "check_iter": self.check_iterator}
        if func not in func_dict.keys():
            raise KeyError(f"No Function of {func} found.")
        else:
            func_dict[func](iterator)

    def iterator_to_string(self, iterator):
        if self.check_iterator(iterator):
            for item in iterator:
                if self.check_iterator(item) and type(item) == tuple:
                    res = list(map(" || ".join, iterator))
                else:
                    new_str = ",".join(iterator)
                    return new_str
            new_str = ",".join(res)
            return new_str

    def check_iterator(self, iterator):
        if type(iterator) == list or type(iterator) == tuple:
            return True
        else:
            return False
