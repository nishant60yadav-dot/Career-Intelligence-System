"""
Configuration Reader
"""

from pathlib import Path

import pandas as pd


class ConfigReader:

    def __init__(self):

        self.file = Path("data/companies.xlsx")

    def load_targets(self):

        return pd.read_excel(
            self.file,
            sheet_name="Battery Job Database"
        )

    def load_keywords(self):

        return pd.read_excel(
            self.file,
            sheet_name="Keywords"
        )