"""
reader.py

Reads configuration files for the Career Intelligence System.
"""

from pathlib import Path

import pandas as pd


class ConfigReader:
    """Reads configuration from Excel files."""

    def __init__(self, data_folder: str = "data"):
        self.data_folder = Path(data_folder)
        self.companies_file = self.data_folder / "companies.xlsx"

    def load_targets(self):
        """Load the Targets sheet."""

        targets = pd.read_excel(
            self.companies_file,
            sheet_name="Targets"
        )

        return targets

    def load_keywords(self):
        """Load the Keywords sheet."""

        keywords = pd.read_excel(
            self.companies_file,
            sheet_name="Keywords"
        )

        return keywords