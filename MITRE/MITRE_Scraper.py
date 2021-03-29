"""
This Package will be to access data from the website to turn into viewable
content. The data will be based on the MITRE ATTACK Framework. It will access
the different types of tatics, techniques and procedures
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from .Utilities import Utilities
import warnings
warnings.filterwarnings("ignore")

HEADER_RE = r"<th.*>(.*)</th>"
GROUPS_URL = "https://attack.mitre.org/groups/"
TITLE_IDX = 0
ASSOC_GRP_IDX = 1
INDEX_ZERO = 0
INDEX_ONE = 1


class Scraper(Utilities):
    def __init__(self):
        self.mitre_grp_url = GROUPS_URL
        self.overview_df = self.find_MITRE_table_data(self.mitre_grp_url)

    def find_MITRE_table_data(self, url):
        results_dict = {
            "Name": [], "Associated Groups": [], 'Description': [], "ID": []}
        mitre_html_group = requests.get(url)
        parsed_html = BeautifulSoup(mitre_html_group.content, 'html.parser')
        table_of_groups = parsed_html.find(
            "table", class_='table table-bordered table-alternate mt-2')
        data = table_of_groups.tbody.find_all("tr")
        for elem in data:
            a_object = elem.find_all("a")[TITLE_IDX]
            assoc_grps = elem.find_all("td")[ASSOC_GRP_IDX].text.strip()
            description = elem.find_all("p").pop().text
            results_dict["Name"].append(
                a_object.text.replace('\n', '').strip())
            if not assoc_grps:
                results_dict["Associated Groups"].append(None)
            else:
                assoc_grps = assoc_grps.split(",")
                assoc_grps_str = self.iterator_to_string(assoc_grps)
                results_dict["Associated Groups"].append(assoc_grps_str)
            results_dict["Description"].append(description)
            results_dict["ID"].append(a_object["href"].strip("/groups/"))
            overview_df = pd.DataFrame(results_dict)
        return overview_df

    def display_all(self, filename=None):
        try:
            if filename is not None:
                self.overview_df.to_csv(filename)
            else:
                return self.overview_df
        except FileNotFoundError:
            raise FileNotFoundError(
                f"{filename} could not be save as directory does not exist.")

    def find(self, group_name):
        res_df = self.overview_df.loc[self.overview_df["Name"] == group_name]
        if res_df.empty:
            return None
        else:
            return res_df
