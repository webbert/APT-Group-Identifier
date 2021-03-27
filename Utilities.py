import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")

TITLE_IDX = 0
ASSOC_GRP_IDX = 1
INDEX_ZERO = 0
INDEX_ONE = 1


def find_MITRE_table_data(url):
    results_dict = {
        "Name": [], "Associated Groups": [], 'Description': [], "ID": []}
    mitre_html_group = requests.get(url)
    parsed_html = BeautifulSoup(mitre_html_group.content, 'html.parser')
    table_of_groups = parsed_html.find(
        "table", class_='table table-bordered table-alternate mt-2')
    data = table_of_groups.tbody.find_all("tr")
    for elem in data:
        a_object = elem.find_all("a")[TITLE_IDX]
        assoc_grps = elem.find_all("td")[ASSOC_GRP_IDX].text.strip().split(",")
        description = elem.find_all("p").pop().text
        results_dict["Name"].append(
            a_object.text.replace('\n', '').strip())
        if assoc_grps is None:
            results_dict["Associated Groups"].append(None)
        else:
            results_dict["Associated Groups"].append(assoc_grps)
        results_dict["Description"].append(description)
        results_dict["ID"].append(a_object["href"].strip("/groups/"))
        overview_df = pd.DataFrame(results_dict)
        overview_df["Associated Groups"] = overview_df["Associated Groups"].apply(
            lambda y: np.nan if len(y) == 0 else y)
    return overview_df


def find_apt_info(url, res_df):
    mitre_html_group = requests.get(url)
    parsed_html = BeautifulSoup(mitre_html_group.content, 'html.parser')
    attack_matrix = parsed_html.find(id="v-attckmatrix")
    block_info = attack_matrix.find_all('div', {"class": "card-data"})
    h_two = attack_matrix.find_all('h2')
    attack_matrix_information_tables = attack_matrix.find_all("table")
    print(attack_matrix_information_tables)
    for info in block_info:
        key = info.text.split(r":")
        key[INDEX_ONE] = key[INDEX_ONE].strip()
        if key[INDEX_ZERO] not in res_df.columns:
            res_df.loc[:, key[INDEX_ZERO]] = key[INDEX_ONE]
        else:
            continue
    return res_df
