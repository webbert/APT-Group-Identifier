"""
The following file will allow the different python classes to use different
utilities for different uses.
"""

import pandas as pd
import numpy as np
import re


class Utilities:
    def __init__(self, func, iterator):
        """Utilities options for use

        Args:
            func (str): Function selected
            iterator (List, Tuple): Iterator to be converted to Pandas
            Dataframe or String

        Raises:
            KeyError: [description]
        """
        func_dict = {"iter_to_str": self.iterator_to_string,
                     "check_iter": self.check_iterator}
        if func not in func_dict.keys():
            raise KeyError(f"No Function of {func} found.")
        else:
            func_dict[func](iterator)

    def iterator_to_str_or_df(self, iterator, column_names=None):
        """Function to convert a iterator to a string or dataframe.

        Args:
            iterator (List or Tuple): Iterator to be converted.
            column_names (list or Numpy array, optional): Column names used in
            the iterator to convert to a Dataframe. Defaults to None.

        Returns:
            str/Pandas.DataFrame: Returns a formatted dataframe or str
        """
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
        """Checks whether the object is an iterator.

        Args:
            iterator (Unknown): Object to check whether it is a iterator.

        Returns:
            bool: True or False whether it is an iterator.
        """
        if type(iterator) == list or type(iterator) == tuple:
            return True
        else:
            return False
