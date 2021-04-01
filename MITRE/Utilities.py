import pandas as pd
import numpy as np
import re


class Utilities:
    def __init__(self, func, iterator):
        func_dict = {"iter_to_str": self.iterator_to_string,
                     "check_iter": self.check_iterator}
        if func not in func_dict.keys():
            raise KeyError(f"No Function of {func} found.")
        else:
            func_dict[func](iterator)

    def iterator_to_str_or_df(self, iterator, column_names=None):
        if self.check_iterator(iterator):
            for item in iterator:
                if self.check_iterator(item) and type(item) == tuple:
                    data_df = pd.DataFrame(iterator, columns=column_names)
                    data_df.replace(r'^\s*$', np.NaN, regex=True, inplace=True)
                    data_df.fillna(method='ffill', inplace=True)
                    if "ID" in data_df.columns:
                        for index in range(len(data_df)):
                            id_check = data_df.loc[index, "ID"]
                            if re.search(r'^/.\d+$', id_check):
                                previous_data = data_df.loc[index - 1, "ID"]
                                tech_ID = re.findall(
                                    r"T\d+", previous_data).pop()
                                new_id = tech_ID + id_check
                                data_df.loc[index, "ID"] = new_id
                    return data_df
                else:
                    new_str = ",".join(iterator)
                    return new_str

    def check_iterator(self, iterator):
        if type(iterator) == list or type(iterator) == tuple:
            return True
        else:
            return False
