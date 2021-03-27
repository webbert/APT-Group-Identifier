"""
This Package will be to access data from the website to turn into viewable
content. The data will be based on the MITRE ATTACK Framework. It will access
the different types of tatics, techniques and procedures
"""

import pandas as pd
from Utilities import find_MITRE_table_data

HEADER_RE = r"<th.*>(.*)</th>"
GROUPS_URL = "https://attack.mitre.org/groups/"


class Scraper():
    def __init__(self):
        self.mitre_grp_url = GROUPS_URL
        self.overview_df = find_MITRE_table_data(self.mitre_grp_url)

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

