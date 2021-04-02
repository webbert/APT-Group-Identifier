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
        """
        Creates the overall MITRE APT Groups table of basic information.
        """
        self.overview_df = self.find_MITRE_table_data(GROUPS_URL)

    def find_MITRE_table_data(self, url):
        """Generates a dataframe with basic information of the different APT
        Groups

        Args:
            url (constant str): Link to MITRE Attack Framework groups url

        Returns:
            Pandas.Dataframe: Overview dataframe containing basic information
            of the different APTs
        """
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
                assoc_grps_str = self.iterator_to_str_or_df(assoc_grps)
                results_dict["Associated Groups"].append(assoc_grps_str)
            results_dict["Description"].append(description)
            results_dict["ID"].append(a_object["href"].strip("/groups/"))
            overview_df = pd.DataFrame(results_dict)
        overview_df.set_index(['Name'], inplace=True)
        return overview_df

    def display_all(self, filename=None):
        """Converts the dataframe to a csv if specified, returns the overall
        basic information dataframe.

        Args:
            filename (str, optional): Filename. Defaults to None.

        Raises:
            FileNotFoundError: Raise error if file name not found

        Returns:
            Pandas.DataFrame: Overview and basic information of all the APTs.
        """
        try:
            if filename is not None:
                self.overview_df.to_csv(filename)
            else:
                return self.overview_df
        except FileNotFoundError:
            raise FileNotFoundError(
                f"{filename} could not be save as directory does not exist.")

    def find(self, group_name):
        """Finds the basic information of the specific APT group.

        Args:
            group_name (str): APT group name

        Returns:
            Pandas.DataFrame: The selected APT group Pandas DataFrame.
        """
        res_df = self.overview_df.loc[[group_name]]
        if res_df.empty:
            return None
        else:
            return res_df
