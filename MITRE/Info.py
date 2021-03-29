import requests.certs
from bs4 import BeautifulSoup
from .MITRE_Scraper import Scraper
from .SQL_Conn import SQL_Conn

GROUPS_URL = "https://attack.mitre.org/groups/"
INDEX_ZERO = 0
INDEX_ONE = 1


class APT_Info(Scraper, SQL_Conn):
    def __init__(self):
        super().__init__()

    def all(self, filename=None):
        res_df = self.display_all(filename)
        return res_df

    def display_apt_info(self, group_name):
        res_df = self.find(group_name)
        ref_link = res_df.iloc[0]["ID"]
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
            column_names = temp_information_table.find_all("th")
            for index_0 in range(len(column_names)):
                list_of_lists_for_data_per_column.append([])
            datastream = temp_information_table.find("tbody")
            row_data = datastream.find_all("tr")
            for index_1 in range(len(row_data)):
                data = row_data[index_1].find_all("td")
                if len(data) == 5:
                    main_link = data.pop(1).text
                    add_link = data[1].text
                    new_link = main_link + "/" + add_link
                    dsata[1].string = new_link
                for index_2 in range(len(data)):
                    # print(data[index_2])
                    # input("asd")
                    if data[index_2].find("a"):
                        list_of_lists_for_data_per_column[index_2].append(
                            data[index_2].find("a").text + ":" + data[index_2].find("a")["href"])
                    else:
                        list_of_lists_for_data_per_column[index_2].append(
                            data[index_2].text.replace("\n", " ").strip(" "))
            zipped_iter = list(zip(*list_of_lists_for_data_per_column))
            formatted_str = self.iterator_to_string(zipped_iter)
            res_df.loc[:, headers[index].text] = [formatted_str]
        self.conn(res_df, group_name)
        return res_df
