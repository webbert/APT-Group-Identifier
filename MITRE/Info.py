"""
Info.py is a python file that allows the use of the Scraper Parent python file
to retrieve the overall basic info which either performs different utilities
such as displaying all APT groups or the all the information of the specific
APT group.
"""

import requests
from bs4 import BeautifulSoup
from .MITRE_Scraper import Scraper

GROUPS_URL = "https://attack.mitre.org/groups/"
INDEX_ZERO = 0
INDEX_ONE = 1


class APT_Info(Scraper):
    def __init__(self):
        """
        Initialise the Parent Class "Scraper".
        """
        Scraper.__init__(self)

    def all(self, filename=None):
        """Returns a dataframe of all of the basic information from the APT groups.

        Args:
            filename (str, optional): filename. Defaults to None.

        Returns:
            Pandas.DataFrame: Overall information of all of the APT groups.
        """
        res_df = self.display_all(filename)
        return res_df

    def display_apt_info(self, group_name):
        """Returns a dictionary of dataframes based on the headers found in
        the webpage of the specific APT group.

        Args:
            group_name (str): Group found in the list of APT groups.

        Returns:
            dict: Dictionary of dataframes based on the headers found in the
            Webpage.
        """
        res_df = self.find(group_name)
        dict_of_res_dfs = {'Basic Info': res_df}
        ref_link = res_df.loc[group_name]["ID"]
        url = GROUPS_URL + str(ref_link)
        mitre_html_group = requests.get(url)
        parsed_html = BeautifulSoup(mitre_html_group.content, 'html.parser')
        attack_matrix = parsed_html.find(id="v-attckmatrix")
        block_info = attack_matrix.find_all('div', {"class": "card-data"})
        headers = attack_matrix.find_all('h2')
        attack_matrix_information_tables = attack_matrix.find_all("table")
        for info in block_info:
            key = info.text.split(r":")
            key[INDEX_ONE] = key[INDEX_ONE].strip()
            if key[INDEX_ZERO] not in res_df.columns:
                res_df.loc[:, key[INDEX_ZERO]] = key[INDEX_ONE]
            else:
                continue
        for index in range(len(attack_matrix_information_tables)):
            temp_information_table = attack_matrix_information_tables[index]
            list_of_lists_for_data_per_column = []
            column_names_encoded = temp_information_table.find_all("th")
            column_names = []
            for index_0 in range(len(column_names_encoded)):
                list_of_lists_for_data_per_column.append([])
                column_names.append(column_names_encoded[index_0].text)
            list_of_lists_for_data_per_column.append([])
            column_names.append("References")
            datastream = temp_information_table.find("tbody")
            row_data = datastream.find_all("tr")
            for index_1 in range(len(row_data)):
                data = row_data[index_1].find_all("td")
                if len(data) == 5:
                    main_link = data.pop(INDEX_ONE).text.strip()
                    add_link = data[INDEX_ONE].text.strip()
                    new_link = main_link + add_link
                    data[INDEX_ONE].string = new_link
                for index_2 in range(len(data)):
                    if data[index_2].find("p"):
                        p_obj = data[index_2].find("p")
                        list_of_lists_for_data_per_column[index_2].append(
                            p_obj.text)
                    elif data[index_2].find_all("a"):
                        list_of_a_objs = data[index_2].find_all("a")
                        data_list = []
                        for a_obj in list_of_a_objs:
                            text_from_obj = a_obj.text.replace(
                                "\n", " ").strip()
                            data_list.append(text_from_obj)
                        full_data_text = ", ".join(data_list)
                        list_of_lists_for_data_per_column[index_2].append(
                            full_data_text)
                    else:
                        list_of_lists_for_data_per_column[index_2].append(
                            data[index_2].text.replace("\n", "").strip())
                    if data[index_2].find_all("a"):
                        list_of_a_objs = data[index_2].find_all("a")
                        reference_final_list = []
                        for a_obj in list_of_a_objs:
                            text_from_obj = a_obj.text.replace(
                                "\n", " ").strip()
                            reference_text = text_from_obj + \
                                ":" + a_obj["href"]
                            reference_final_list.append(reference_text)
                reference_final_text = ", ".join(reference_final_list)
                list_of_lists_for_data_per_column[-1].append(
                    reference_final_text)
            zipped_iter = list(zip(*list_of_lists_for_data_per_column))
            formatted = self.iterator_to_str_or_df(zipped_iter, column_names)
            dict_of_res_dfs[headers[index].text] = formatted
        return dict_of_res_dfs
